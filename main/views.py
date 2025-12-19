from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods
from .models import Program, Participant, Document, Course, Quiz, Video, Test, Certification
from .forms import ProgramForm, ParticipantForm


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
