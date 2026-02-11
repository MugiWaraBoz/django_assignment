from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from datetime import date

from events.models import Participant,Event,Category
# from user.forms import 

# Create your views here.
def sign_in(request):
    form = AuthenticationForm()
    context = {
        'form' : form,
    }
    return render(request, 'registration/sign-in.html', context)

def sign_up(request):
    form = UserCreationForm()
    context = {
        'form' : form,
    }
    return render(request, 'registration/sign-in.html', context)

def sign_out(request):
    pass