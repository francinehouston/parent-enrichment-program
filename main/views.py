from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.db import models as django_models
from .models import Program, Participant, Document, Course, Quiz, Video, Test, Certification, MemberDocument, VendorSubmission, Donation, FundDistribution, DataVaultItem
from .forms import ProgramForm, ParticipantForm, UserRegistrationForm, DocumentUploadForm, VendorSubmissionForm
from decimal import Decimal


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


@require_http_methods(["GET", "POST"])
def vendor(request):
    """Vendor page"""
    if request.method == 'POST':
        form = VendorSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your submission! We will review your service offering and get back to you soon.')
            return redirect('main:vendor')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VendorSubmissionForm()
    
    return render(request, 'vendor.html', {'vendor_form': form})


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
    from django.db.models import Sum
    
    total_donations = Donation.objects.filter(status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    total_distributed = FundDistribution.objects.filter(status='DISTRIBUTED').aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    available_funds = total_donations - total_distributed
    
    stats = {
        'documents': Document.objects.count(),
        'courses': Course.objects.count(),
        'quizzes': Quiz.objects.count(),
        'videos': Video.objects.count(),
        'tests': Test.objects.count(),
        'certifications': Certification.objects.count(),
        'total_donations': total_donations,
        'total_distributed': total_distributed,
        'available_funds': available_funds,
        'pending_distributions': FundDistribution.objects.filter(status='PENDING').count(),
        'approved_vendors': VendorSubmission.objects.filter(is_approved=True).count(),
        'vault_items': DataVaultItem.objects.count(),
    }
    return render(request, 'admin/dashboard.html', {'stats': stats})


@staff_member_required
def fund_distribution_list(request):
    """List all fund distributions"""
    distributions = FundDistribution.objects.all().select_related('donation', 'vendor', 'created_by', 'approved_by')
    return render(request, 'admin/fund_distributions/list.html', {'distributions': distributions})


@staff_member_required
@require_http_methods(["GET", "POST"])
def fund_distribution_new(request):
    """Create a new fund distribution"""
    from django.db.models import Sum
    
    if request.method == 'POST':
        donation_id = request.POST.get('donation')
        vendor_id = request.POST.get('vendor')
        amount = request.POST.get('amount')
        purpose = request.POST.get('purpose')
        notes = request.POST.get('notes', '')
        
        try:
            donation = Donation.objects.get(id=donation_id, status='COMPLETED')
            vendor = VendorSubmission.objects.get(id=vendor_id, is_approved=True)
            amount_decimal = Decimal(amount)
            
            # Check if distribution amount doesn't exceed available funds from this donation
            existing_distributions = FundDistribution.objects.filter(donation=donation, status__in=['PENDING', 'APPROVED', 'DISTRIBUTED']).aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            available_from_donation = donation.amount - existing_distributions
            
            if amount_decimal > available_from_donation:
                messages.error(request, f'Distribution amount (${amount_decimal}) exceeds available funds from this donation (${available_from_donation}).')
                return redirect('main:fund_distribution_new')
            
            distribution = FundDistribution.objects.create(
                donation=donation,
                vendor=vendor,
                amount=amount_decimal,
                purpose=purpose,
                notes=notes,
                created_by=request.user,
                status='PENDING'
            )
            messages.success(request, f'Fund distribution of ${amount_decimal} to {vendor.service_name} has been created and is pending approval.')
            return redirect('main:fund_distribution_list')
        except (Donation.DoesNotExist, VendorSubmission.DoesNotExist, ValueError) as e:
            messages.error(request, 'Invalid donation or vendor selected, or invalid amount.')
    
    # Get available donations and approved vendors
    available_donations = Donation.objects.filter(status='COMPLETED').order_by('-donated_at')
    approved_vendors = VendorSubmission.objects.filter(is_approved=True).order_by('service_name')
    
    return render(request, 'admin/fund_distributions/new.html', {
        'donations': available_donations,
        'vendors': approved_vendors,
    })


@staff_member_required
@require_http_methods(["GET", "POST"])
def fund_distribution_approve(request, distribution_id):
    """Approve a fund distribution"""
    distribution = get_object_or_404(FundDistribution, id=distribution_id)
    
    if request.method == 'POST':
        if distribution.status == 'PENDING':
            distribution.status = 'APPROVED'
            distribution.approved_by = request.user
            distribution.save()
            messages.success(request, f'Fund distribution of ${distribution.amount} has been approved.')
        else:
            messages.error(request, 'Only pending distributions can be approved.')
    
    return redirect('main:fund_distribution_list')


@staff_member_required
@require_http_methods(["GET", "POST"])
def fund_distribution_distribute(request, distribution_id):
    """Mark a fund distribution as distributed"""
    from django.utils import timezone
    
    distribution = get_object_or_404(FundDistribution, id=distribution_id)
    
    if request.method == 'POST':
        if distribution.status == 'APPROVED':
            distribution.status = 'DISTRIBUTED'
            distribution.distributed_at = timezone.now()
            distribution.save()
            messages.success(request, f'Fund distribution of ${distribution.amount} has been marked as distributed.')
        else:
            messages.error(request, 'Only approved distributions can be marked as distributed.')
    
    return redirect('main:fund_distribution_list')
