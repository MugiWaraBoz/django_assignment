from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

from datetime import date

from events.models import Participant,Event,Category
from user.forms import CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.
def sign_in(request):
    form = CustomAuthenticationForm()
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print(form)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in {username}")
                return redirect("dashboard")
            
    context = {
        'form' : form,
    }
    return render(request, 'registration/sign-in.html', context)

def sign_up(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully")
            return redirect("dashboard")

    context = {
        'form' : form,
    }
    return render(request, 'registration/sign-up.html', context)

def sign_out(request):
    messages.success(request, "Log Out Successfully")
    logout(request)
    # if request.method == 'POST':
    return redirect("dashboard")