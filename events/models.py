from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Participant(models.Model):
    event = models.ManyToManyField(
        "Event",
        related_name = "participants")

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name

class Event(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    date = models.DateField(_("Event Date"))
    time = models.TimeField(_("Event Time"))
    location = models.CharField(_("Event Location"), max_length=250)
    category = models.ForeignKey(
        "Category", 
        on_delete=models.CASCADE,
        related_name = "events")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name