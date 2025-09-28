# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from allauth.account.models import EmailAddress

# Unregister default models
admin.site.unregister(SocialAccount)
admin.site.unregister(SocialApp)
admin.site.unregister(SocialToken)
admin.site.unregister(EmailAddress)

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'profile_picture')
        }),
        (_('Additional info'), {
            'fields': ('user_group', 'activity_date')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2'),
        }),
    )
    
    list_display = ('username', 'email', 'phone_number', 'user_group', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'user_group')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number')
    ordering = ('username',)

# Social Account Admins (simplified)
@admin.register(SocialAccount)
class SocialAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'uid')
    list_filter = ('provider',)
    search_fields = ('user__username', 'user__email', 'uid')

@admin.register(SocialApp)
class SocialAppAdmin(admin.ModelAdmin):
    list_display = ['name', 'provider']
    filter_horizontal = ['sites']

@admin.register(SocialToken)
class SocialTokenAdmin(admin.ModelAdmin):
    list_display = ['account', 'app', 'expires_at']
    list_filter = ['app__provider']

# Email Address Admin
@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ['email', 'user', 'primary', 'verified']
    list_filter = ['primary', 'verified']
    search_fields = ['email', 'user__username']