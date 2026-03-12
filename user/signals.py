from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User, Group
from decouple import config
from event_management import settings
  
@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        # print("✅ User Created")
        token = default_token_generator.make_token(instance)
        activation_url = (
            f"{config('FRONTEND_URL')}/user/activate/{instance.id}/{token}"
        )
        try:
            # print("✅ Email sended")
            send_mail(
                subject="Activate Your Account",
                message=f"Please activate your account using the following link :{activation_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
            )
        except Exception as e:
            print(f"❌ There was an error sending the activation link, please try again. {e}")

@receiver(post_save, sender=User)
def pass_change_email(sender, instance, created, **kwargs):
    pass