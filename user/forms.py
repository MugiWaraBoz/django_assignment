from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from events.forms import MixinStyleForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(MixinStyleForm, UserCreationForm):
    print("User Creation Form Loaded ✅")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]
    
class userCreationForm(MixinStyleForm, form.ModelForm):

    class Meta:
        model = User
        fields = ["Usernae", "email", "first_name", "last_name", "password", "confirm_password"]
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        password_c = self.cleaned_data.get("confirm_password")
        errors = []

        if(password != password_c){
            errors.add("Password mismatch");
            raise.vali
        }

        return password
    

class CustomAuthenticationForm(MixinStyleForm, AuthenticationForm):
    print("Authentication Form Loaded ✅")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

