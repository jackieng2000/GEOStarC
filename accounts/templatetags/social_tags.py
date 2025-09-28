from django import template
from allauth.socialaccount.models import SocialAccount

register = template.Library()

@register.filter
def is_google_user(user):
    """
    Template filter to check if user is a Google user
    Usage: {% if user|is_google_user %}
    """
    if not user or user.is_anonymous:
        return False
    return SocialAccount.objects.filter(user=user, provider='google').exists()

@register.filter
def social_provider(user):
    """
    Template filter to get social provider
    Usage: {{ user|social_provider }}
    """
    if not user or user.is_anonymous:
        return 'email'
    social_account = SocialAccount.objects.filter(user=user).first()
    return social_account.provider if social_account else 'email'

@register.simple_tag
def get_registration_badge(user):
    """
    Template tag to display registration method badge
    Usage: {% get_registration_badge user %}
    """
    if not user or user.is_anonymous:
        return ''
    
    social_account = SocialAccount.objects.filter(user=user).first()
    
    if social_account:
        provider = social_account.provider
        if provider == 'google':
            return '<span class="badge bg-danger">Google</span>'
        elif provider == 'github':
            return '<span class="badge bg-dark">GitHub</span>'
        else:
            return f'<span class="badge bg-info">{provider.title()}</span>'
    else:
        return '<span class="badge bg-primary">Email</span>'