from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_images = models.ImageField(upload_to='profile_images/', blank=True, null=True) 
    bio = models.TextField(blank=True, null=True)

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_img = models.ImageField(upload_to="profile_images/", null=True, blank=True)
#     def __str__(self):
#         return f"{self.user.username}"