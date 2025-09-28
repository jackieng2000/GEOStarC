# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress

class CustomUser(AbstractUser):
    # Custom fields
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    user_group = models.CharField(max_length=15, blank=True, help_text="User group (15 characters max)")
    activity_date = models.DateField(null=True, blank=True, help_text="Date of current activity")
    
    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to.'),
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="customuser_permissions_set",
        related_query_name="customuser",
    )
    
    def __str__(self):
        return self.email or self.username
    
    def delete(self, *args, **kwargs):
        # Delete associated EmailAddress records first
        EmailAddress.objects.filter(user=self).delete()
        # Then delete the user
        super().delete(*args, **kwargs)