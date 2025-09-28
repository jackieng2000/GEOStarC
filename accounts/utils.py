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