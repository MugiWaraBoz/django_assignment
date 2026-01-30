from django.contrib import admin
from django.urls import path, include
from events.views import dashboard, event_details

urlpatterns = [
    path('dashboard/', dashboard),
    path('details/', event_details),
]
