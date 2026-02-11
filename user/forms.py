from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from events.forms import MixinStyleForm
from django.contrib.auth.models import User

class CustomUserCreationForm(MixinStyleForm, UserCreationForm):
    print("User Creation Form Loaded ✅")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
    


class CustomAuthenticationForm(MixinStyleForm, AuthenticationForm):
    print("Authentication Form Loaded ✅")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

