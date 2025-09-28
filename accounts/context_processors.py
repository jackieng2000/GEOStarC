from allauth.socialaccount.models import SocialAccount

def is_google_user(user):
    """
    Check if a user registered via Google
    Returns True if user registered with Google, False otherwise
    """
    if not user or user.is_anonymous:
        return False
    return SocialAccount.objects.filter(user=user, provider='google').exists()

def get_social_provider(user):
    """
    Get the social provider name for a user
    Returns provider name (e.g., 'google', 'github') or None if not social user
    """
    if not user or user.is_anonymous:
        return None
    social_account = SocialAccount.objects.filter(user=user).first()
    return social_account.provider if social_account else None

def get_user_registration_method(user):
    """
    Get the registration method for a user
    Returns 'google', 'github', 'email', or None
    """
    if not user or user.is_anonymous:
        return None
    social_account = SocialAccount.objects.filter(user=user).first()
    return social_account.provider if social_account else 'email'

# def user_registration_info(request):
#     """
#     Add user registration information to template context
#     """
#     context = {}
    
#     if request.user.is_authenticated:
#         context['is_google_user'] = is_google_user(request.user)
#         context['social_provider'] = get_social_provider(request.user)
#         context['registration_method'] = get_user_registration_method(request.user)
    
#     return context

from django.apps import apps

def user_registration_info(request):
    """
    Add user registration information to template context
    Safely handles cases where SocialAccount model might not be available
    """
    context = {}
    
    if request.user.is_authenticated:
        try:
            # Check if SocialAccount model is available
            if apps.is_installed('allauth.socialaccount'):
                from allauth.socialaccount.models import SocialAccount
                
                user = request.user
                
                # Check if Google user
                is_google = SocialAccount.objects.filter(user=user, provider='google').exists()
                context['is_google_user'] = is_google
                
                # Get social provider
                social_account = SocialAccount.objects.filter(user=user).first()
                context['social_provider'] = social_account.provider if social_account else None
                
                # Get registration method
                context['registration_method'] = social_account.provider if social_account else 'email'
            else:
                # Fallback if allauth is not available
                context['is_google_user'] = False
                context['social_provider'] = None
                context['registration_method'] = 'email'
                
        except ImportError:
            # Handle case where allauth is not properly installed
            context['is_google_user'] = False
            context['social_provider'] = None
            context['registration_method'] = 'email'
    
    return context