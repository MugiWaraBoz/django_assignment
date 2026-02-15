from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete, m2m_changed