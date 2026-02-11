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
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully")
            return redirect("dashboard")

    context = {
        'form' : form,
    }
    return render(request, 'registration/sign-in.html', context)

def sign_up(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        print("Post Request Recived ✅")
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
    if request.method == 'POST':
        messages.success(request, "Log Out Successfully")
        logout(request)
    return redirect("dashboard")