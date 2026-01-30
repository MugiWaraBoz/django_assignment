from django.contrib import admin
from django.urls import path, include
from events.views import dashboard, event_details,event_form

urlpatterns = [
    path('dashboard/', dashboard, name = "dashboard"),
    path('details/', event_details, name = "event-details"),
    path("add-events/", event_form, name = "event_form"),
]
