# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from rest_framework.permissions import AllowAny  # Add this line

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings

import logging

logger = logging.getLogger(__name__)

from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny



# accounts/views.py
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmation
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

@method_decorator(csrf_exempt, name='dispatch')
class CustomConfirmEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, key):
        try:
            confirmation = EmailConfirmation.objects.get(key=key)
            confirmation.confirm(request)
            return JsonResponse({
                'success': True, 
                'message': 'Email verified successfully'
            })
        except EmailConfirmation.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'Invalid confirmation key'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=400)

# Also add a view to resend confirmation email
@method_decorator(csrf_exempt, name='dispatch')
class ResendVerificationEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return JsonResponse({
                'success': False, 
                'error': 'Email is required'
            }, status=400)
        
        try:
            from allauth.account.models import EmailAddress
            from django.contrib.auth import get_user_model
            from allauth.account.utils import send_email_confirmation
            
            User = get_user_model()
            user = User.objects.get(email=email)
            email_address = EmailAddress.objects.get_for_user(user, email)
            
            if email_address.verified:
                return JsonResponse({
                    'success': False, 
                    'error': 'Email is already verified'
                }, status=400)
            
            send_email_confirmation(request, user, email=email)
            return JsonResponse({
                'success': True, 
                'message': 'Verification email sent'
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'error': 'User with this email does not exist'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            }, status=400)




@method_decorator(ensure_csrf_cookie, name='dispatch')
class EnsureCSRFTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return JsonResponse({'status': 'CSRF cookie set'})


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse

@method_decorator(csrf_exempt, name='dispatch')
class CustomPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        User = get_user_model()
        users = User.objects.filter(email=email)
        
        if not users.exists():
            # Return success for security (don't reveal if email exists)
            return Response(
                {'message': 'If that email address is registered, you will receive a password reset link.'},
                status=status.HTTP_200_OK
            )
        
        try:
            for user in users:
                # Generate password reset token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Build reset URL - point to your frontend
                reset_url = f"http://localhost:5173/geo_pages1/password-reset-confirm/{uid}/{token}/"
                
                # Email content
                subject = "Password Reset Request"
                message = f"""
                Hello {user.username},
                
                You're receiving this email because you requested a password reset for your GEOStarA account.
                
                Please click the link below to reset your password:
                {reset_url}
                
                If you didn't request this, please ignore this email.
                
                Thank you,
                GEOStarA Team
                """
                
                # Send email
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            
            return Response(
                {'message': 'If that email address is registered, you will receive a password reset link.'},
                status=status.HTTP_200_OK
            )
                
        except Exception as e:
            print(f"Password reset error: {str(e)}")
            return Response(
                {'error': 'Failed to send reset email. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )        
            
            
            
from accounts.utils import is_google_user, get_social_provider

def user_profile(request):
    user = request.user
    context = {
        'is_google_user': is_google_user(user),
        'social_provider': get_social_provider(user),
    }
    return render(request, 'profile.html', context)

def admin_dashboard(request):
    from django.contrib.auth.models import User
    from accounts.utils import is_google_user
    
    users = User.objects.all()
    user_stats = []
    
    for user in users:
        user_stats.append({
            'username': user.username,
            'email': user.email,
            'is_google_user': is_google_user(user),
            'provider': get_social_provider(user),
        })
    
    context = {'user_stats': user_stats}
    return render(request, 'admin_dashboard.html', context)



from django.contrib.auth.decorators import login_required
from .utils import is_google_user, get_social_provider

@login_required
def registration_info(request):
    """
    Display user's registration information
    """
    user = request.user
    context = {
        'is_google_user': is_google_user(user),
        'social_provider': get_social_provider(user),
        'registration_method': get_user_registration_method(user),
    }
    return render(request, 'accounts/registration_info.html', context)

from django.views.generic import TemplateView

class EmailConfHelpView(TemplateView):
    template_name = 'account/email_confirmation_help.html'

