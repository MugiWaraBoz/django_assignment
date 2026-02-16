from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from decouple import config
from datetime import date


from events.models import Event, RSVP, User
from event_management import settings

# New Event Signal
@receiver(post_save, sender=Event)
def new_event_added(sender, created, instance, **kwargs):
    if created :
        current_date = date.today()
        emails = User.objects.values_list("email", flat=True)
        
        if emails and instance.date >= current_date:
            try:
                send_mail(
                    subject="New Event Created",
                    message=f"New event created, RSVP now! {instance.name}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=emails
                )
            except Exception as e:
                print(f"❌ Error sending new event emails:  {e}")

# RSVP Signal
@receiver(post_save, sender=RSVP)
def RSVP_a_event(sender, created, instance, **kwargs):
    if created :
        curr_user = instance.participants
        token = default_token_generator.make_token(curr_user)
        activation_url = (
            f"{config('FRONTEND_URL')}/rsvp/{instance.id}/{token}"
        )

        try:
            send_mail(
                subject="RSVP Event",
                message=f"Click the following link to RSVP the event: {activation_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[curr_user.email],
            )
        except Exception as e:
            print(f"❌ Error sending RSVP activation email: {e}")
