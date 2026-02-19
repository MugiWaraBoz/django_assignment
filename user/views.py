from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, login_not_required
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Prefetch


from datetime import date

from events.models import RSVP, Event,Category
from events.views import is_admin, is_Organizer, is_participant
from user.forms import CustomAuthenticationForm, userCreationForm
from user.models import Profile

# Create your views here.
@login_not_required
def sign_in(request):
    form = CustomAuthenticationForm()
    if request.method == "POST":
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in {username}")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password")
                return render(request, "registration/sign-in.html", {'form' : form})
            
    return render(request, "registration/sign-in.html", {'form' : form})

@login_not_required
def sign_up(request):
    form = userCreationForm()

    if request.method == "POST":
        form = userCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get("password"))
            user.is_active = False
            user.save()

            profile = Profile.objects.create(
                user=user,
                profile_img=form.cleaned_data.get("profile_img")
            )
            profile.save()
            role = form.cleaned_data.get("role")
            if role :
                group, created = Group.objects.get_or_create(name=role)
                user.groups.add(group)

            messages.success(request, f"Check you email for Activation")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    
    context = {
        'form' : form,
    }
    return render(request, 'registration/sign-up.html', context)

@login_required(login_url="home")
def sign_out(request):
    messages.success(request, "Log Out Successfully")
    logout(request)
    # if request.method == 'POST':
    return redirect("dashboard")

@login_not_required
def no_permission(request):
    return render(request, "no-permission.html")

def activate_account(request, uid, token):
    try:
        # print("✅ Activation Success")
        user = User.objects.get(id=uid)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                "Your account has been activated successfully! You can now log in."
            )
            return redirect("sign-in")
        else:
            messages.error(request, "Invalid activation link.")
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request, "Invalid Activation Link")
        return redirect("home")

# ADMIN DASHBOARD VIEWS

@login_required(login_url="home")
@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    return render(request, "dashboards/admin-dashboard.html")

@login_required(login_url="home")
@user_passes_test(is_admin, login_url="no-permission")
def manage_roles(request):
    users = User.objects.prefetch_related('groups')

    context = {
        "users" : users,
    }
    
    return render(request, "dashboards/admin/manage-roles.html", context)

@login_required(login_url="home")
@user_passes_test(is_admin, login_url="no-permission")
def change_user_group(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        new_group_name = request.POST.get("group")
        if new_group_name:
            new_group, created = Group.objects.get_or_create(name=new_group_name)
            user.groups.clear()
            user.groups.add(new_group)
            messages.success(request, f"{user.username} is now a {new_group_name}")
        else:
            messages.error(request, "No group selected.")
    return redirect("manage-roles")

@login_required(login_url="home")
@user_passes_test(is_admin, login_url="no-permission")
def organizers(request):
    organizers = User.objects.select_related('profile').prefetch_related('groups', 'events').filter(groups__name="Organizer")
    organizers = organizers.annotate(event_organized_count=Count('events', distinct=True))
    context = {
        "organizers" : organizers,
    }
    return render(request, "dashboards/admin/organizers.html", context)

@login_required(login_url="home")
@user_passes_test(is_admin, login_url="no-permission")
def participants(request):
    participants = User.objects.select_related('profile').prefetch_related('groups', 'events', 'rsvp').filter(groups__name="Participants")
    participants = participants.annotate(event_participated_count=Count('rsvp__event', distinct=True))
    context = {
        "participants" : participants
    }
    return render(request, "dashboards/admin/participants.html", context)

@login_required(login_url="home")
@user_passes_test(is_admin, login_url="no-permission")
def role_details(request):
    groups = Group.objects.prefetch_related("permissions").all()
            
    context = {
        "groups" : groups,
    }
    return render(request, "dashboards/admin/role-details.html", context)

@login_required(login_url="home")
@user_passes_test(is_admin, login_url="no-permission")
def manage_all_events(request):
    events = Event.objects.prefetch_related('organizers').all()
    context = {
        "events": events,
    }
    return render(request, "dashboards/admin/manage-all-events.html", context)

@login_required(login_url="home")
@user_passes_test(is_admin, login_url="no-permission")
def admin_view_rsvps(request):
    all_rsvps = RSVP.objects.select_related('event', 'participants').filter(participants=request.user)
    return render(request, "dashboards/admin/view-rsvps.html", {"rsvps": all_rsvps})

# ORGANIZER DASHBOARD VIEWS
@login_required(login_url="home")
@user_passes_test(is_Organizer, login_url="no-permission")
def organizer_dashboard(request, id):       
    return render(request, "dashboards/organizer-dashboard.html", {"id": id})   

@login_required(login_url="home")
@user_passes_test(is_Organizer, login_url="no-permission")
def manage_events(request, id):
    events = Event.objects.prefetch_related('organizers').filter(organizers__id=id)
    context = {
        "events": events,
    }
    return render(request, "dashboards/organizer/manage-events.html", context)   

@login_required(login_url="home")
@user_passes_test(is_Organizer, login_url="no-permission")
def view_rsvps(request, id):
    rsvp_events = RSVP.objects.select_related('event', 'participants').filter(participants_id=id)
    return render(request, "dashboards/organizer/view-rsvps.html", {"id": id, "events": rsvp_events})

@login_required(login_url="home")
@user_passes_test(lambda u : is_Organizer(u) or is_admin(u), login_url="no-permission")
def create_event_org(request, id):
    return render(request, "dashboards/organizer/event_creation.html", {"id": id})




# USER DASHBOARD VIEWS
@login_required(login_url="home")
@user_passes_test(is_participant, login_url="no-permission")
def user_dashboard(request, id): 
    return render(request, "dashboards/user-dashboard.html", {"id": id})


@login_required(login_url="home")
@user_passes_test(is_participant, login_url="no-permission")
def usr_view_rsvps(request, id):
    rsvps = RSVP.objects.select_related('event', 'participants').filter(participants__id=id)
    return render(request, "dashboards/user/view-rsvps.html", {"id": id, "rsvps": rsvps})


    