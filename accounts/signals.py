# accounts/signals.py
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    messages.success(request, 'You have successfully logged in!')
    
# In your signals.py (create if it doesn't exist)


@receiver(pre_delete, sender=User)
def delete_allauth_email_addresses(sender, instance, **kwargs):
    """Delete AllAuth email addresses when a user is deleted"""
    EmailAddress.objects.filter(user=instance).delete()