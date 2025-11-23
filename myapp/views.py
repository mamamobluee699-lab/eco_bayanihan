from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import FieldError
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date, datetime
import time
import json

from .forms import CleanupEventForm, ParticipantForm, ParticipantRegistrationForm, VolunteerLoginForm
from .models import Participant, CleanupEvent, CleanupRegistration, Activity


@user_passes_test(lambda u: u.is_staff, login_url='myapp:admin_login')
def custom_admin_panel(request):
    # Update activity timestamp on each page visit
    request.session['admin_last_activity'] = time.time()
    
    events = CleanupEvent.objects.all().order_by('-date')
    participants = Participant.objects.all()

    return render(request, 'myapp/custom_admin_panel.html', {
        'events': events,
        'participants': participants,
    })


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            request.session['admin_last_activity'] = time.time()
            return redirect('myapp:custom_admin_panel')
        else:
            messages.error(request, "Invalid admin credentials")

    return render(request, "myapp/admin_login.html")


def admin_logout(request):
    logout(request)
    request.session.flush()
    return redirect('myapp:admin_login')


def event_participants(request, event_id):
    event = get_object_or_404(CleanupEvent, id=event_id)
    participants = Participant.objects.filter(cleanupregistration__event=event)

    context = {
        'event': event,
        'participants': participants,
    }
    return render(request, 'myapp/event_participants.html', context)


def add_event(request):
    request.session['admin_last_activity'] = time.time()
    
    if request.method == 'POST':
        form = CleanupEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.is_active = True
            event.is_completed = False
            if request.user.is_authenticated:
                event.created_by = request.user
            event.save()
            messages.success(request, "Event added successfully!")
            return redirect('myapp:custom_admin_panel')
    else:
        form = CleanupEventForm()
    return render(request, 'myapp/admin_add_edit.html', {'form': form, 'title': 'Add Event'})


def edit_event(request, event_id):
    request.session['admin_last_activity'] = time.time()
    
    event = get_object_or_404(CleanupEvent, id=event_id)
    if request.method == 'POST':
        form = CleanupEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('myapp:custom_admin_panel')
    else:
        form = CleanupEventForm(instance=event)
    return render(request, 'myapp/admin_add_edit.html', {'form': form, 'title': 'Edit Event'})


def delete_event(request, event_id):
    request.session['admin_last_activity'] = time.time()
    
    event = get_object_or_404(CleanupEvent, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect('myapp:custom_admin_panel')


def add_participant(request):
    request.session['admin_last_activity'] = time.time()
    
    if request.method == 'POST':
        form = ParticipantRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant added successfully!")
            return redirect('myapp:custom_admin_panel')
    else:
        form = ParticipantRegistrationForm()
    return render(request, 'myapp/admin_add_edit.html', {'form': form, 'title': 'Add Participant'})


def edit_participant(request, participant_id):
    request.session['admin_last_activity'] = time.time()
    
    participant = get_object_or_404(Participant, id=participant_id)
    if request.method == 'POST':
        form = ParticipantRegistrationForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant updated successfully!")
            return redirect('myapp:custom_admin_panel')
    else:
        form = ParticipantRegistrationForm(instance=participant)
    return render(request, 'myapp/admin_add_edit.html', {'form': form, 'title': 'Edit Participant'})


def delete_participant(request, participant_id):
    request.session['admin_last_activity'] = time.time()
    
    participant = get_object_or_404(Participant, id=participant_id)

    if request.method == "POST":
        participant.delete()
        return redirect('myapp:custom_admin_panel')

    return render(request, "myapp/confirm_delete.html", {"participant": participant})


def give_points(request, participant_id):
    request.session['admin_last_activity'] = time.time()
    
    participant = get_object_or_404(Participant, id=participant_id)
    if request.method == 'POST':
        points = int(request.POST.get('points', 0))
        participant.points += points
        participant.save()
        
        request.session[f'points_added_{participant.email}'] = {
            'points': points,
            'total_points': participant.points
        }
        
        messages.success(request, f"{points} points added to {participant.fullname}.")
        return redirect('myapp:custom_admin_panel')

    return render(request, 'myapp/give_points.html', {'participant': participant})


def select_event(request):
    participant = None
    participant_email = request.session.get('participant_email')
    if participant_email:
        try:
            participant = Participant.objects.get(email=participant_email)
        except Participant.DoesNotExist:
            participant = None

    today = date.today()

    previous_events = CleanupEvent.objects.filter(date__lt=today).annotate(
        registered_count=Count('cleanupregistration')
    ).order_by('-date')
    current_events = CleanupEvent.objects.filter(date=today).annotate(
        registered_count=Count('cleanupregistration')
    ).order_by('start_time')
    upcoming_events = CleanupEvent.objects.filter(date__gt=today).annotate(
        registered_count=Count('cleanupregistration')
    ).order_by('date')

    if request.method == 'POST' and participant:
        event_id = request.POST.get('event')
        if not event_id:
            messages.error(request, "Please select an event first.")
        else:
            event = get_object_or_404(CleanupEvent, id=event_id)

            already_registered = CleanupRegistration.objects.filter(
                participant=participant, event=event
            ).exists()

            if already_registered:
                messages.warning(request, "You have already registered for this event.")
            else:
                CleanupRegistration.objects.create(participant=participant, event=event)
                request.session['registration_success'] = {
                    'event_name': event.name,
                    'event_place': event.place,
                    'event_specific_location': event.specific_location,
                    'event_date': event.date.strftime("%B %d, %Y"),
                    'event_start_time': event.start_time.strftime("%I:%M %p"),
                    'event_duration': event.duration,
                    'event_points': event.points
                }
                return redirect('myapp:select_event')

    registration_success = request.session.pop('registration_success', None) if request.method == 'GET' else None

    context = {
        'participant': participant,
        'previous_events': previous_events,
        'current_events': current_events,
        'upcoming_events': upcoming_events,
        'registration_success': registration_success
    }
    return render(request, 'myapp/select_event.html', context)


def previous_events_list(request):
    today = date.today()
    events = CleanupEvent.objects.filter(date__lt=today).order_by('-date')

    search_query = request.GET.get('q', '').strip()
    date_filter = request.GET.get('date', '').strip()

    if search_query:
        events = events.filter(
            Q(name__icontains=search_query) |
            Q(place__icontains=search_query) |
            Q(specific_location__icontains=search_query)
        )

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            events = events.filter(date=filter_date)
        except ValueError:
            date_filter = ''

    context = {
        'events': events,
        'search_query': search_query,
        'date_filter': date_filter,
    }
    return render(request, 'myapp/previous_events.html', context)


def event_list(request):
    today = date.today()

    previous_events = CleanupEvent.objects.filter(date__lt=today).order_by('-date')
    current_events = CleanupEvent.objects.filter(date=today).order_by('start_time')
    upcoming_events = CleanupEvent.objects.filter(date__gt=today).order_by('date')

    context = {
        'previous_events': previous_events,
        'current_events': current_events,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'myapp/event_list.html', context)


def register(request):
    if request.method == 'POST':
        form = ParticipantRegistrationForm(request.POST)
        if form.is_valid():
            try:
                participant = form.save(commit=False)
                if participant.email:
                    participant.email = participant.email.strip().lower()
                raw_pw = form.cleaned_data.get('password', '').strip()
                participant.password = make_password(raw_pw)
                participant.save()
                messages.success(request, "Registration successful. You can now log in.")
                return redirect('myapp:volunteer_login')
            except Exception as e:
                messages.error(request, f"Registration failed: {e}")
        else:
            messages.error(request, "Registration failed. Please check the highlighted fields.")
    else:
        form = ParticipantRegistrationForm()

    return render(request, 'myapp/register.html', {'form': form})


def volunteer_login(request):
    form = VolunteerLoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data['identifier'].strip()
        raw_pw = form.cleaned_data['password'].strip()

        admin_user = authenticate(request, username=identifier, password=raw_pw)
        if admin_user and admin_user.is_staff:
            login(request, admin_user)
            request.session.pop('participant_email', None)
            request.session['admin_last_activity'] = time.time()
            messages.success(request, "Welcome back, admin!")
            return redirect('myapp:custom_admin_panel')

        email_identifier = identifier.strip().lower()
        try:
            participant = Participant.objects.get(email__iexact=email_identifier)
        except Participant.DoesNotExist:
            messages.error(request, "Invalid credentials. Please check your email/username and password.")
        else:
            if check_password(raw_pw, participant.password):
                request.session['participant_email'] = participant.email
                messages.success(request, "Login successful! Select your event below.")
                return redirect('myapp:select_event')
            messages.error(request, "Invalid credentials. Please check your email/username and password.")

    return render(request, 'myapp/volunteer_login.html', {'form': form})


def home(request):
    return render(request, 'myapp/home.html')


def about(request):
    return render(request, 'myapp/about.html')


def register_success(request):
    return render(request, 'myapp/register_success.html')


def volunteer_logout(request):
    logout(request)
    request.session.flush()
    return redirect('myapp:volunteer_login')


def volunteer_dashboard(request):
    return render(request, 'myapp/volunteer_dashboard.html')


def status_lookup(request):
    return render(request, 'myapp/status_lookup.html')


def upload_proof(request, registration_id):
    return render(request, 'myapp/upload_proof.html', {'registration_id': registration_id})


def approve_registration(request, registration_id):
    messages.success(request, f'Registration {registration_id} approved!')
    return redirect('myapp:home')


def registration_success(request, event_id):
    event = get_object_or_404(CleanupEvent, id=event_id)
    return render(request, 'myapp/registration_success.html', {'event': event})


def points_history(request):
    participant_email = request.session.get('participant_email')
    if not participant_email:
        return render(request, 'myapp/points_history.html', {'points_history': [], 'total_points': 0})

    try:
        participant = Participant.objects.get(email=participant_email)
    except Participant.DoesNotExist:
        return render(request, 'myapp/points_history.html', {'points_history': [], 'total_points': 0})

    registrations = CleanupRegistration.objects.filter(participant=participant, attended=True)
    points_history_data = []
    total_points = 0
    
    for reg in registrations:
        awarded_by = "Not yet awarded"
        awarded_at = None
        
        if reg.points_awarded and reg.approved:
            if reg.approved_by:
                awarded_by = reg.approved_by.username if reg.approved_by.username else reg.approved_by.email
            else:
                awarded_by = "Admin"
            awarded_at = reg.approved_at
            event_points = reg.event.points
            total_points += event_points
        else:
            event_points = 0
        
        points_history_data.append({
            'event': reg.event,
            'points': event_points,
            'awarded_by': awarded_by,
            'awarded_at': awarded_at,
            'registered_at': reg.registered_at,
            'points_awarded': reg.points_awarded and reg.approved
        })

    return render(request, 'myapp/points_history.html', {
        'points_history': points_history_data,
        'total_points': total_points
    })


def combined_list(request):
    participant_email = request.session.get('participant_email')
    if not participant_email:
        return render(request, 'myapp/combined_history.html', {'combined_history': []})

    try:
        participant = Participant.objects.get(email=participant_email)
    except Participant.DoesNotExist:
        return render(request, 'myapp/combined_history.html', {'combined_history': []})

    registrations = CleanupRegistration.objects.filter(participant=participant).order_by('-registered_at')
    combined_history_data = []
    
    for reg in registrations:
        points_value = 0
        points_status = "Pending"
        
        if reg.points_awarded:
            points_status = "Awarded"
            points_value = reg.event.points
        
        combined_history_data.append({
            'event_name': reg.event.name,
            'event_date': reg.event.date,
            'event_time': reg.event.start_time,
            'points': points_value,
            'points_status': points_status,
            'attended': reg.attended,
            'registered_at': reg.registered_at,
            'type': 'event'
        })

    total_points = participant.points
    
    return render(request, 'myapp/combined_history.html', {
        'combined_history': combined_history_data,
        'total_points': total_points,
        'participant_points': participant.points
    })