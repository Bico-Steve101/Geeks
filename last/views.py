# from django.contrib.sites import requests
import requests
from django.urls import reverse
import math
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.core.serializers import serialize
import json
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserForm, HackathonForm, ContactForm, ProjectForm, GradeForm, GradeFormSet

from last.models import Projects, Team, Hackathons, Grade, User, Contacts


# Create your views here.


def index(request):
    # Get the first 6 objects for each model
    geeksTeam = Team.objects.all()
    project = Projects.objects.all()[:4]
    hackathons = Hackathons.objects.all()[:4]

    context = {
        'geeksTeam': geeksTeam,
        'hackathons': hackathons,
        'project': project
    }
    return render(request, 'base.html', context)


def get_recent_activities():
    # Fetch the latest projects and hackathons
    recent_projects = Projects.objects.order_by('-created_at')[:3]
    recent_hackathons = Hackathons.objects.order_by('-created')[:3]

    # Format the information into dictionaries
    project_activities = [
        {
            "category": "New Project",
            "title": project.title,
            "timestamp": project.created_at,
        }
        for project in recent_projects
    ]

    hackathon_activities = [
        {
            "category": "New Hackathon",
            "title": hackathon.name,
            "timestamp": hackathon.created,
        }
        for hackathon in recent_hackathons
    ]

    # Combine and return the activities
    return project_activities + hackathon_activities


def format_time_since(time):
    now = timezone.now()
    diff = now - time

    if diff.days == 0 and 0 <= diff.seconds < 60:
        seconds = diff.seconds
        return f"{seconds} {'second' if seconds == 1 else 'seconds'} ago"
    elif diff.days == 0 and 60 <= diff.seconds < 3600:
        minutes = math.floor(diff.seconds / 60)
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
    elif diff.days == 0 and 3600 <= diff.seconds < 86400:
        hours = math.floor(diff.seconds / 3600)
        return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
    elif 1 <= diff.days < 30:
        days = diff.days
        return f"{days} {'day' if days == 1 else 'days'} ago"
    elif 30 <= diff.days < 365:
        months = math.floor(diff.days / 30)
        return f"{months} {'month' if months == 1 else 'months'} ago"
    elif diff.days >= 365:
        years = math.floor(diff.days / 365)
        return f"{years} {'year' if years == 1 else 'years'} ago"


def dashboard(request):
    # Retrieve data for the dashboard
    user_count = User.objects.count()
    active_user_count = User.objects.filter(last_login__gte=timezone.now() - timedelta(days=30)).count()
    project_count = Projects.objects.count()
    hackathon_count = Hackathons.objects.count()
    recent_projects = Projects.objects.order_by('-created_at')[:5]
    upcoming_hackathons = Hackathons.objects.filter(start_date__gte=timezone.now())[:5]
    recent_activities = get_recent_activities()
    for activity in recent_activities:
        activity["time_since"] = format_time_since(activity["timestamp"])

    # Format time since creation for recent projects
    for project in recent_projects:
        project.time_since_created = format_time_since(project.created_at)

    # Format time until start for upcoming hackathons
    for hackathon in upcoming_hackathons:
        hackathon.time_until_start = format_time_since(hackathon.start_date)

    # Retrieve all users for the user section
    users = User.objects.all()
    # Search functionality
    query = request.GET.get('search')
    highlight_user = None
    highlight_project = None
    highlight_hackathon = None

    if query:
        # Search for users, projects, and hackathons
        user_match = users.filter(username__icontains=query).first()
        project_match = Projects.objects.filter(Q(title__icontains=query) | Q(description__icontains=query)).first()
        hackathon_match = Hackathons.objects.filter(name__icontains=query).first()

        # Determine the section to highlight based on the matches
        if user_match:
            highlight_user = user_match.username
        elif project_match:
            highlight_project = project_match.title
        elif hackathon_match:
            highlight_hackathon = hackathon_match.name

    user_data = [
        {"username": user.username, "projects_count": user.projects.count()} for user in users
    ]

    context = {
        'user_count': user_count,
        'active_user_count': active_user_count,
        'project_count': project_count,
        'hackathon_count': hackathon_count,
        'recent_projects': recent_projects,
        'upcoming_hackathons': upcoming_hackathons,
        'recent_activities': recent_activities,
        'users': users,
        'user_data_json': json.dumps(user_data),
        'highlight_user': highlight_user,
        'highlight_project': highlight_project,
        'highlight_hackathon': highlight_hackathon,
    }

    return render(request, 'dashboard.html', context)


def all_projects(request):
    # Get all objects for projects
    project = Projects.objects.all()[:4]
    hackathons = Hackathons.objects.all()[:4]
    projects = Projects.objects.all()
    context = {
        'project': project,
        'hackathons': hackathons,
        'projects': projects,
    }
    return render(request, 'all_projects.html', context)


def all_hackathons(request):
    # Get all objects for hackathons
    project = Projects.objects.all()[:4]
    hackathon = Hackathons.objects.all()[:4]
    hackathons = Hackathons.objects.all()
    context = {
        'project': project,
        'hackathon': hackathon,
        'hackathons': hackathons,
    }
    return render(request, 'all_hackathons.html', context)


def hackathon_detail(request, hackathon_id):
    project = Projects.objects.all()[:4]
    hackathons = Hackathons.objects.all()[:4]
    hackathon = Hackathons.objects.get(pk=hackathon_id)
    grades = Grade.objects.filter(hackathon=hackathon)
    participants = hackathon.participants.all().order_by('username')

    # No need to fetch JSON report data here

    context = {
        'hackathon': hackathon,
        'participants': participants,
        'grades': grades,
        'hackathons': hackathons,
        'project': project,
        # 'report_data': report_data,  # No need to include report_data here
    }

    return render(request, 'hackathons.html', context)


def download_hackathon_report(request, hackathon_id):
    hackathon = get_object_or_404(Hackathons, pk=hackathon_id)
    grades = Grade.objects.filter(hackathon=hackathon)

    # Convert data to a JSON-serializable format
    report_data = {
        'hackathon_name': hackathon.name,
        'participants': [{'username': grade.participant.username, 'grade': str(grade.grade)} for grade in grades],
    }

    # Create a JSON response
    response = JsonResponse(report_data, safe=False)

    # Set response headers to make it a downloadable file
    response['Content-Disposition'] = f'attachment; filename={hackathon.name}_report.json'

    return response


@login_required(login_url='/login')
def join_hackathon(request, hackathon_id):
    hackathon = get_object_or_404(Hackathons, pk=hackathon_id)
    # Check if the user is authenticated (logged in)
    if request.user.is_authenticated:
        # Add the logged-in user to the participants of the hackathon
        hackathon.participants.add(request.user)
        # You can also perform additional checks or operations here
        # For instance, you might want to check if the user is already a participant before adding them
    return redirect('last:hackathon_details', hackathon_id=hackathon_id)


# def grade_participant(request, hackathon_id, participant_id):
#     hackathon = get_object_or_404(Hackathons, pk=hackathon_id)
#
#     # Check if the current user is the hackathon founder
#     if request.user == hackathon.founder:
#         participant = get_object_or_404(User, pk=participant_id)
#         grade, created = Grade.objects.get_or_create(hackathon=hackathon, participant=participant)
#
#         if request.method == 'POST':
#             form = GradeForm(request.POST, instance=grade)
#             if form.is_valid():
#                 form.save()
#                 return redirect('hackathon_details', hackathon_id=hackathon_id)
#         else:
#             form = GradeForm(instance=grade)
#
#         return render(request, 'registration/grade_participant.html',
#         {'form': form, 'participant': participant, 'hackathon': hackathon})
#     else:
#         return HttpResponse("You are not authorized to grade participants in this hackathon.")
#

@login_required(login_url='/login')
def grade_participant(request, hackathon_id, participant_id):
    hackathon = get_object_or_404(Hackathons, pk=hackathon_id)

    if request.user == hackathon.founder:
        participant = get_object_or_404(User, pk=participant_id)
        try:
            grade = Grade.objects.get(hackathon=hackathon, participant=participant)
        except Grade.DoesNotExist:
            grade = None

        if request.method == 'POST':
            form = GradeForm(request.POST, instance=grade)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.hackathon = hackathon
                instance.participant = participant
                instance.save()
                return redirect('last:hackathon_details', hackathon_id=hackathon_id)
        else:
            form = GradeForm(instance=grade)

        return render(request, 'registration/grade_participant.html', {'form': form,
                                                                       'participant': participant,
                                                                       'hackathon': hackathon})
    else:
        return HttpResponse("You are not authorized to grade participants in this hackathon.")


@login_required(login_url='/login')
def grade_all_participants(request, hackathon_id):
    hackathon = get_object_or_404(Hackathons, pk=hackathon_id)
    participants = hackathon.participants.all()

    if request.method == 'POST':
        for participant in participants:
            form = GradeForm(request.POST)
            if form.is_valid():
                grade_instance, _ = Grade.objects.get_or_create(hackathon=hackathon, participant=participant)
                grade_instance.grade = form.cleaned_data['grade']
                grade_instance.save()
        return redirect('hackathon_details', hackathon_id=hackathon_id)
    else:
        form = GradeForm()

    return render(request, 'registration/grade_all_participants.html',
                  {'participants': participants, 'hackathon': hackathon, 'form': form})


@login_required(login_url='/login')
def add_hackathon(request):
    if request.method == 'POST':
        form = HackathonForm(request.POST, request.FILES)
        if form.is_valid():
            # Assign the current user as the founder of the hackathon
            hackathon = form.save(commit=False)
            hackathon.founder = request.user
            hackathon.save()
            return redirect('last:hackathon_details',
                            hackathon_id=hackathon.id)  # Redirect to the hackathon detail view after creation
    else:
        form = HackathonForm()

    return render(request, 'registration/add_hackathon.html', {'form': form})


@login_required(login_url='/login')
def updateHackathon(request, hackathon_id):
    hackathons = get_object_or_404(Hackathons, id=hackathon_id)

    if request.method == 'POST':
        form = HackathonForm(request.POST, request.FILES, instance=hackathons)
        if form.is_valid():
            form.save()
            return redirect('last:hackathon_details', hackathon_id=hackathons.id)
    else:
        form = HackathonForm(instance=hackathons)

    return render(request, 'registration/update_hackathon.html', {'form': form, 'hackathons': hackathons})


@login_required(login_url='/login')
def delete_hackathon(request, hackathon_id):
    hackathon = get_object_or_404(Hackathons, id=hackathon_id)
    if request.method == 'POST':
        hackathon.delete()
        # Redirect to a specific URL after deleting the hackathon, for example, the hackathon list
        return redirect('last:index')
    return render(request, 'registration/confirm_hackathon_delete.html', {'hackathon': hackathon})


# def hackathons(request):
#     hackathons = Hackathons.objects.all()
#
#     if request.method == 'GET':
#         hackathon_id = request.GET.get('hackathon_id')
#         if hackathon_id is not None:
#             hackathon = Hackathons.objects.get(id=hackathon_id)
#             return redirect('hackathon_details', hackathon.id)
#
#     participants = []
#
#     for hackathon in hackathons:
#         grades = Grade.objects.filter(hackathon=hackathon)
#         for grade in grades:
#             participant = {
#                 'avatar': grade.user.avatar,
#                 'username': grade.user.username,
#                 'grade': grade.grade,
#             }
#             participants.append(participant)
#
#     context = {
#         'hackathons': hackathons,
#         'participants': participants,
#     }
#
#     return render(request, 'hackathons.html', context)
#

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('last:profile', pk=user.pk)  # Redirect to the user's profile or any other desired page
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        # Assuming you have 'username', 'password', and 'email' fields in your form
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(request, username=username, password=password, email=email)

        if user is not None:
            login(request, user)
            messages.success(request, 'You have successfully logged in.')
            return redirect(
                '/')  # You might want to replace 'base.html' with the actual URL or view name you want to redirect to after login
        else:
            messages.error(request, 'Failed to log in. Please check your credentials.')
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')


def user_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')


# def projects(request, pk):
#     project = Projects.objects.get(id=pk)
#     context = {
#         'project': project
#     }
#
#     return render(request, 'profile.html', context)


# def grades(request, pk):
#     user_grade = Grade.objects.get(id=pk)
#     context = {
#         'user_grade': user_grade
#     }
#     return render(request, 'profile.html', context)
#

# def teams(request, pk):
#     team = Team.objects.get(id=pk)
#     context = {
#         'team': team
#     }
#     return render(request, 'profile.html', context)


# def contacts(request, pk):
#     contact = Contacts.objects.get(id=pk)
#     context = {
#         'contact': contact
#     }
#     return render(request, 'profile.html', context)


def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    hackathon = Hackathons.objects.filter(founder=user)
    project = Projects.objects.filter(user=user)
    team = Team.objects.filter(user=user)
    contact = Contacts.objects.filter(user=user)

    projects_count = project.count()
    hackathon_count = hackathon.count()

    context = {
        'user': user,
        'project': project,
        'team': team,
        'contact': contact,
        'hackathon': hackathon,
        'projects_count': projects_count,
        'hackathon_count': hackathon_count
    }

    return render(request, 'profile.html', context)


@login_required(login_url='/login')
def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('last:profile', pk=user.id)
    return render(request, 'registration/edit-profile.html', {'form': form})


@login_required(login_url='/login')
def delete_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        # Redirect to a specific URL after deleting the user profile, for example, the home page
        return redirect('last:index')
    return render(request, 'registration/confirm_profile_delete.html', {'user': user})


@login_required(login_url='/login')
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user  # Set the current user as the project's user
            project.save()
            return redirect('last:index')
    else:
        form = ProjectForm()

    return render(request, 'registration/add_project.html', {'form': form})


@login_required(login_url='/login')
def edit_project(request, project_id):
    project = get_object_or_404(Projects, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('last:index')  # Redirect to the desired page after editing
    else:
        form = ProjectForm(instance=project)

    return render(request, 'registration/edit_project.html', {'form': form, 'project': project})


@login_required(login_url='/login')
def delete_project(request, project_id):
    project = get_object_or_404(Projects, id=project_id)
    if request.method == 'POST':
        project.delete()
        # Redirect to a specific URL after deleting the project, for example, the project list
        return redirect('last:index')
    return render(request, 'registration/confirm_project_delete.html', {'project': project})


@login_required(login_url='/login')
def add_contact(request):
    user = request.user
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user  # Assign the current user to the contact
            contact.save()
            return redirect('last:profile',
                            pk=user.id)  # Redirect to a success page or any desired page after adding the contact
    else:
        form = ContactForm()
    return render(request, 'registration/add_contact.html', {'form': form})


@login_required(login_url='/login')
def delete_contact(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contacts, id=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect('last:profile',
                        pk=user.id)

        # If it's not a POST request, render a confirmation page
    return render(request, 'registration/confirm_delete_contact.html', {'contact': contact})


@login_required(login_url='/login')
def edit_contact(request, contact_id):
    user = request.user
    contact = get_object_or_404(Contacts, id=contact_id)

    if request.user != contact.user:
        return HttpResponse('You are not the owner of this contact!')

    form = ContactForm(instance=contact)

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('last:profile',
                            pk=user.id)  # Redirect to the contact detail view

    return render(request, 'registration/edit_contact.html', {'form': form, 'contact': contact})


def members(request):
    user = User.objects.all()
    projects = Projects.objects.all()[:4]
    geeksTeam = Team.objects.all()
    hackathons = Hackathons.objects.all()[:4]
    context = {
        'user': user,
        'projects': projects,
        'geeksTeam': geeksTeam,
        'hackathons': hackathons
    }
    return render(request, 'members.html', context)


def error_404_view(request, exception=None):
    return render(request, '404.html', status=404)


def error_403_view(request, exception=None):
    return render(request, '403.html', status=403)


def error_401_view(request, exception=None):
    return render(request, '401.html', status=401)


def error_400_view(request, exception=None):
    return render(request, '400.html', status=400)


def error_500_view(request, exception=None):
    return render(request, '500.html', status=500)
