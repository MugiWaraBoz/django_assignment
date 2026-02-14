from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
# class Participant(models.Model):

#     name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=254)

#     def __str__(self):
#         return self.name


class Event(models.Model):

    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    description = models.TextField()
    location = models.CharField(_("Event Location"), max_length=250)
    date = models.DateField(_("Event Date"))
    time = models.TimeField(_("Event Time"))
    category = models.ForeignKey(
        "Category", 
        on_delete=models.CASCADE,
        related_name = "events")

    participants = models.ManyToManyField(
        User,
        # "Participant",
        related_name = "events")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


class RSVP(models.Model):

    event = models.ForeignKey(
        "Event",
        on_delete=models.CASCADE,
        related_name="rsvp"
    )

    participants = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name = "rsvp",
    )

    is_going = models.BooleanField(default=True)

    def __str__(self):
        return super().__str__()

