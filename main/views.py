from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .models import Program, Participant, Document, Course, Quiz, Video, Test, Certification, MemberDocument
from .forms import ProgramForm, ParticipantForm, UserRegistrationForm, DocumentUploadForm


def index(request):
    """Home page"""
    programs = Program.objects.all()[:5]  # Show latest 5
    participant_count = Participant.objects.count()
    return render(request, 'index.html', {
        'programs': programs,
        'participant_count': participant_count
    })


def about(request):
    """About page"""
    return render(request, 'about.html')


def list_programs(request):
    """List all programs"""
    programs = Program.objects.all()
    return render(request, 'programs.html', {'programs': programs})


def program_detail(request, program_id):
    """View a single program"""
    program = get_object_or_404(Program, id=program_id)
    return render(request, 'program_detail.html', {'program': program})


@require_http_methods(["GET", "POST"])
def new_program(request):
    """Create a new program"""
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program created successfully!')
            return redirect('list_programs')
    else:
        form = ProgramForm()
    return render(request, 'new_program.html', {'form': form})


def list_participants(request):
    """List all participants"""
    participants = Participant.objects.all()
    return render(request, 'participants.html', {'participants': participants})


@require_http_methods(["GET", "POST"])
def new_participant(request):
    """Register a new participant"""
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant registered successfully!')
            return redirect('list_participants')
    else:
        form = ParticipantForm()
    return render(request, 'new_participant.html', {'form': form})


def membership(request):
    """Membership page"""
    return render(request, 'membership.html')


def vendor(request):
    """Vendor page"""
    return render(request, 'vendor.html')


@require_http_methods(["GET", "POST"])
def upload_document(request):
    """Handle document uploads for membership pre-qualification"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get or create participant based on email
            email = request.POST.get('participant_email')
            if email:
                participant, created = Participant.objects.get_or_create(
                    email=email,
                    defaults={
                        'name': request.POST.get('participant_name', ''),
                        'phone': request.POST.get('participant_phone', ''),
                        'children_ages': request.POST.get('participant_children_ages', ''),
                    }
                )
                document = form.save(commit=False)
                document.participant = participant
                document.save()
                messages.success(request, f'Document uploaded successfully! Your {document.get_document_type_display()} has been received.')
                return redirect('main:membership')
            else:
                messages.error(request, 'Please provide your email address.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DocumentUploadForm()
    
    return render(request, 'membership.html', {'document_form': form})


@require_http_methods(["GET", "POST"])
def donate(request):
    """Donate page"""
    # Handle PayPal return URLs
    if request.GET.get('success') == '1':
        messages.success(request, 'Thank you for your donation! Your support makes a difference. You should receive a confirmation email from PayPal shortly.')
    elif request.GET.get('cancel') == '1':
        messages.error(request, 'Your donation was cancelled. If you experienced any issues, please try again or contact us for assistance.')
    
    if request.method == 'POST':
        messages.success(request, 'Thank you for your donation! Your support makes a difference.')
        return redirect('donate')
    
    return render(request, 'donate.html')


@csrf_protect
@require_http_methods(["GET", "POST"])
def register(request):
    """User registration page"""
    # If user is already logged in, redirect to home
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('main:index')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {user.username}!')
            return redirect('main:index')
        else:
            # Form has errors, they will be displayed in the template
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'admin/register.html', {'form': form})


@csrf_protect
@require_http_methods(["GET", "POST"])
def admin_login(request):
    """Custom admin login page"""
    # If user is already logged in and is staff, redirect to dashboard
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('main:admin_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    # Redirect to next page if specified, otherwise go to dashboard
                    next_url = request.GET.get('next', 'main:admin_dashboard')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Access denied. Staff privileges required.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please enter both username and password.')
    
    return render(request, 'admin/login.html')


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard"""
    stats = {
        'documents': Document.objects.count(),
        'courses': Course.objects.count(),
        'quizzes': Quiz.objects.count(),
        'videos': Video.objects.count(),
        'tests': Test.objects.count(),
        'certifications': Certification.objects.count(),
    }
    return render(request, 'admin/dashboard.html', {'stats': stats})
