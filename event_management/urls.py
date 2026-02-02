from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('events.urls')),
]

# Serve media files in development
if settings.DEBUG or True:  # Serve media regardless of DEBUG for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
