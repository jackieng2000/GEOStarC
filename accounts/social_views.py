# accounts/social_views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.github.provider import GitHubProvider
import requests

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """
    Handle Google OAuth login and return JWT tokens
    """
    try:
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response(
                {'error': 'Access token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the access token with Google
        google_response = requests.get(
            f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={access_token}'
        )
        
        if google_response.status_code != 200:
            return Response(
                {'error': 'Invalid access token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        google_data = google_response.json()
        email = google_data.get('email')
        name = google_data.get('name', '')
        google_id = google_data.get('id')
        
        if not email:
            return Response(
                {'error': 'Email not provided by Google'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': email,
                'first_name': name.split(' ')[0] if name else '',
                'last_name': ' '.join(name.split(' ')[1:]) if len(name.split(' ')) > 1 else '',
                'is_active': True,
            }
        )
        
        # Create or update social account
        social_account, created = SocialAccount.objects.get_or_create(
            user=user,
            provider=GoogleProvider.id,
            defaults={'uid': google_id}
        )
        
        if not created:
            social_account.uid = google_id
            social_account.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token_jwt = str(refresh.access_token)
        refresh_token_jwt = str(refresh)
        
        return Response({
            'access': access_token_jwt,
            'refresh': refresh_token_jwt,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Authentication failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def google_auth_url(request):
    """
    Get Google OAuth URL for frontend
    """
    from django.conf import settings
    from urllib.parse import urlencode
    
    # You'll need to set these in your environment variables
    client_id = getattr(settings, 'GOOGLE_OAUTH2_CLIENT_ID', '')
    
    if not client_id:
        return Response(
            {'error': 'Google OAuth not configured'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    params = {
        'client_id': client_id,
        'redirect_uri': f"{request.scheme}://{request.get_host()}/accounts/google/login/callback/",
        'scope': 'openid email profile',
        'response_type': 'code',
        'access_type': 'offline',
        'prompt': 'consent',
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    
    return Response({
        'auth_url': auth_url
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def github_login(request):
    """
    Handle GitHub OAuth login and return JWT tokens
    """
    try:
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response(
                {'error': 'Access token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the access token with GitHub
        github_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}
        )
        
        if github_response.status_code != 200:
            return Response(
                {'error': 'Invalid access token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        github_data = github_response.json()
        github_id = github_data.get('id')
        username = github_data.get('login', '')
        name = github_data.get('name', '')
        
        # Get user email from GitHub (may require additional API call)
        email_response = requests.get(
            'https://api.github.com/user/emails',
            headers={'Authorization': f'token {access_token}'}
        )
        
        email = None
        if email_response.status_code == 200:
            emails = email_response.json()
            # Find primary email
            for email_data in emails:
                if email_data.get('primary', False):
                    email = email_data.get('email')
                    break
            # If no primary email, use the first one
            if not email and emails:
                email = emails[0].get('email')
        
        # If still no email, use GitHub username as email
        if not email:
            email = f"{username}@github.local"
        
        if not email:
            return Response(
                {'error': 'Email not provided by GitHub'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username or email,
                'first_name': name.split(' ')[0] if name else username,
                'last_name': ' '.join(name.split(' ')[1:]) if len(name.split(' ')) > 1 else '',
                'is_active': True,
            }
        )
        
        # Create or update social account
        social_account, created = SocialAccount.objects.get_or_create(
            user=user,
            provider=GitHubProvider.id,
            defaults={'uid': str(github_id)}
        )
        
        if not created:
            social_account.uid = str(github_id)
            social_account.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token_jwt = str(refresh.access_token)
        refresh_token_jwt = str(refresh)
        
        return Response({
            'access': access_token_jwt,
            'refresh': refresh_token_jwt,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Authentication failed: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def github_auth_url(request):
    """
    Get GitHub OAuth URL for frontend
    """
    from django.conf import settings
    from urllib.parse import urlencode
    
    # You'll need to set these in your environment variables
    client_id = getattr(settings, 'GITHUB_OAUTH2_CLIENT_ID', '')
    
    if not client_id:
        return Response(
            {'error': 'GitHub OAuth not configured'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    params = {
        'client_id': client_id,
        'redirect_uri': f"{request.scheme}://{request.get_host()}/accounts/github/login/callback/",
        'scope': 'user:email',
        'response_type': 'code',
    }
    
    auth_url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
    
    return Response({
        'auth_url': auth_url
    }, status=status.HTTP_200_OK)

