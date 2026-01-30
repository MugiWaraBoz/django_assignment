from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin-2243/', admin.site.urls),
    path('events/', include('events.urls')),
]
