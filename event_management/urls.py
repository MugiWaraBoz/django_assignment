from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import home, error_404
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('user/', include('user.urls')),
    path('home/', home, name='home'),
    path('error-404/', error_404, name='error-404'),
]

# Serve media files in development
if settings.DEBUG:  # Serve media regardless of DEBUG for development
    urlpatterns += debug_toolbar_urls()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)