# mobile_auth/views.py
import logging
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from allauth.socialaccount.models import SocialAccount

logger = logging.getLogger(__name__)

class MobileLoginView(APIView):
    """Simple JWT login for React Native - no sessions"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            logger.info(f"Mobile login successful for user: {user.username}")
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            })
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class MobileRegisterView(APIView):
    """Simple registration for React Native - returns JWT tokens"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response(
                {'error': 'Username, email, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"Mobile user registered: {username}")
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(f"Mobile registration error: {str(e)}")
            return Response({'error': 'Registration failed'}, status=status.HTTP_400_BAD_REQUEST)

# Inclu
# de MobileGoogleLoginView and MobileGitHubLoginView from previous example...

class MobileGoogleLoginView(APIView):
    """
    Google login for React Native using ID tokens from mobile Google Sign-In
    """
    permission_classes = [AllowAny]

    def post(self, request):
        id_token = request.data.get('id_token')  # From React Native Google Sign-In

        if not id_token:
            return Response(
                {'error': 'No ID token provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Verify ID token with Google
            token_response = requests.get(
                f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}'
            )

            if token_response.status_code != 200:
                return Response(
                    {'error': 'Invalid Google token'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_data = token_response.json()
            email = user_data.get('email')

            if not email:
                return Response(
                    {'error': 'Email not provided by Google'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            User = get_user_model()

            # Find or create user
            try:
                social_account = SocialAccount.objects.get(uid=user_data['sub'], provider='google')
                user = social_account.user
            except SocialAccount.DoesNotExist:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    # Create new user
                    username = email.split('@')[0]
                    # Ensure unique username
                    base_username = username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}{counter}"
                        counter += 1
                    
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        first_name=user_data.get('given_name', ''),
                        last_name=user_data.get('family_name', '')
                    )
                
                # Create social account
                SocialAccount.objects.create(
                    user=user,
                    uid=user_data['sub'],
                    provider='google',
                    extra_data=user_data
                )

            # Generate JWT tokens (no session creation)
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"Mobile Google login successful for user: {user.username}")

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"Mobile Google login error: {str(e)}")
            return Response(
                {'error': 'Google authentication failed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


class MobileGitHubLoginView(APIView):
    """
    GitHub login for React Native using access tokens from mobile OAuth
    """
    permission_classes = [AllowAny]

    def post(self, request):
        access_token = request.data.get('access_token')  # From React Native GitHub OAuth

        if not access_token:
            return Response(
                {'error': 'No access token provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get user info from GitHub
            user_response = requests.get(
                'https://api.github.com/user',
                headers={
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/vnd.github.v3+json',
                },
                timeout=30
            )

            if user_response.status_code != 200:
                return Response(
                    {'error': 'Failed to get user info from GitHub'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_data = user_response.json()
            
            # Get user emails
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers={
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/vnd.github.v3+json',
                },
                timeout=30
            )
            
            emails = email_response.json() if email_response.status_code == 200 else []
            primary_email = next((email['email'] for email in emails if email['primary'] and email['verified']), None)
            
            if not primary_email:
                return Response(
                    {'error': 'No verified primary email found for GitHub user'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            User = get_user_model()
            
            # Find or create user
            try:
                social_account = SocialAccount.objects.get(uid=user_data['id'], provider='github')
                user = social_account.user
            except SocialAccount.DoesNotExist:
                try:
                    user = User.objects.get(email=primary_email)
                except User.DoesNotExist:
                    username = user_data.get('login', primary_email.split('@')[0])
                    # Ensure unique username
                    base_username = username
                    counter = 1
                    while User.objects.filter(username=username).exists():
                        username = f"{base_username}{counter}"
                        counter += 1
                    
                    user = User.objects.create_user(
                        username=username,
                        email=primary_email,
                        first_name=user_data.get('name', '').split(' ')[0] if user_data.get('name') else '',
                        last_name=' '.join(user_data.get('name', '').split(' ')[1:]) if user_data.get('name') else '',
                    )
                
                # Create social account
                SocialAccount.objects.create(
                    user=user,
                    uid=user_data['id'],
                    provider='github',
                    extra_data=user_data
                )

            # Generate JWT tokens (no session creation)
            refresh = RefreshToken.for_user(user)

            logger.info(f"Mobile GitHub login successful for user: {user.username}")

            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"Mobile GitHub login error: {str(e)}")
            return Response(
                {'error': 'GitHub authentication failed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )