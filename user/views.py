from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test, login_not_required
from django.contrib.auth.tokens import default_token_generator

from datetime import date

from events.models import Event,Category
from user.forms import CustomAuthenticationForm, userCreationForm

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

def activate_account(request, uid, token):
    try:
        print("✅ Activation Success")
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

def user_dashboard(request, id): 
    return render(request, "dashboards/user-dashboard.html")
    
def admin_dashboard(request, id):
    return render(request, "dashboards/admin-dashboard.html")



def organizer_dashboard(request, id):       
    return render(request, "dashboards/organizer-dashboard.html")            
