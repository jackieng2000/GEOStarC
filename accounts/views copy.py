# account/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from accounts.utils import is_google_user, get_social_provider, get_user_registration_method
from .forms import RegisterForm, LoginForm

import logging

logger = logging.getLogger(__name__)

@method_decorator(ensure_csrf_cookie, name='dispatch')
class EnsureCSRFTokenView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return JsonResponse({'status': 'CSRF cookie set'})

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

def user_profile(request):
    user = request.user
    context = {
        'is_google_user': is_google_user(user),
        'social_provider': get_social_provider(user),
    }
    return render(request, 'profile.html', context)

def admin_dashboard(request):
    from django.contrib.auth.models import User
    
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

class EmailConfHelpView(TemplateView):
    template_name = 'account/email_confirmation_help.html'