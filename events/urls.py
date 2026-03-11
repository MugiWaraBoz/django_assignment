from django.urls import path, include
from events.views import event_detailsView ,delete_eventView ,edit_eventView, event_formView, rsvp_event, rsvp_removed, rsvp_activation
from events.views import dashboardClassView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('', dashboard, name = "dashboard"),
    path('', dashboardClassView.as_view(), name = "dashboard"),
    # path('details/<int:event_id>/', event_details, name = "event-details"),
    path('details/<int:event_id>/', event_detailsView.as_view() , name = "event-details"),
    # path("add-events/by/<int:usr_id>/", event_form, name = "event_form"),
    path("add-events/by/<int:usr_id>/", event_formView.as_view() , name = "event_form"),
    # path("delete-event/<int:event_id>/", delete_event, name="delete-event"),
    path("delete-event/<int:event_id>/", delete_eventView.as_view(), name="delete-event"),
    # path("edit-event/<int:event_id>/", edit_event, name="edit-event"),
    path("edit-event/<int:event_id>/", edit_eventView.as_view(), name="edit-event"),
    path("rsvp/<int:event_id>/", rsvp_event, name="rsvp"),
    path("rsvp/remove/<int:event_id>/", rsvp_removed, name="rsvp_r"),
    path("rsvp/<int:uid>/<str:token>/", rsvp_activation, name="rsvp_activation")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)