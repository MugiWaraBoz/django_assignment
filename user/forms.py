import re
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
    
class userCreationForm(MixinStyleForm, forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    profile_img = forms.ImageField(required=False, label="Profile Image")
    
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password", "confirm_password" ,"profile_img"]
    
    def clean_password(self):
        password = self.cleaned_data.get("password")
        errors = []

        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")

        elif not re.search(r"[A-Z]", password):
            errors.append("Password must contain at least one uppercase letter.")

        elif not re.search(r"[a-z]", password):
            errors.append("Password must contain at least one lowercase letter.")

        elif not re.search(r"[0-9]", password):
            errors.append("Password must contain at least one digit.")

        elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            errors.append("Password must contain at least one special character.")
            
        if errors :
            raise forms.ValidationError(errors)
        
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_c = cleaned_data.get("confirm_password")

        if password and password_c and password != password_c:
            raise ValidationError("Password and Confirm password mismatch")

        return cleaned_data

class CustomAuthenticationForm(MixinStyleForm, AuthenticationForm):
    print("Authentication Form Loaded ✅")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

