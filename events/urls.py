from django.contrib import admin
from django.urls import path, include
from events.views import dashboard, event_details,event_form, delete_event, edit_event

urlpatterns = [
    path('dashboard/', dashboard, name = "dashboard"),
    path('details/<int:event_id>/', event_details, name = "event-details"),
    path("add-events/", event_form, name = "event_form"),
    path("delete-event/<int:event_id>/", delete_event, name="delete-event"),
    path("edit-event/<int:event_id>/", edit_event, name="edit-event"),
]