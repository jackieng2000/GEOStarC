from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny  # Add this line
from gpsinfo.views import GPSLocationViewSet
from pages.views import GpsTestView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, get_user_model, login
import requests
import logging
from django.conf import settings
from allauth.account.views import PasswordResetView 
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.models import SocialAccount

# urls.py - Add this import at the top with other imports
from accounts.views import CustomPasswordResetView  # Add this line
from accounts.views import CustomPasswordResetView, EnsureCSRFTokenView  # Add EnsureCSRFTokenView

# Remove this line from urlpatterns:
# path('api/auth/password/reset/', 'accounts.views.CustomPasswordResetView.as_view()', name='api_password_reset'),

# # Replace with this:

# Set up logging
logger = logging.getLogger(__name__)

router = DefaultRouter()
router.register(r'gpslocations', GPSLocationViewSet, basename='gpslocation')

class CustomLoginView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            logger.info(f"Custom login successful for user: {user.username}")
            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username
            }, status=status.HTTP_200_OK)
        logger.error(f"Custom login failed: invalid credentials for username {username}")
        return Response({'non_field_errors': ['Invalid credentials']}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response(
                {'non_field_errors': ['Username, email, and password are required']},
                status=status.HTTP_400_BAD_REQUEST
            )

        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'username': ['A user with that username already exists.']},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'email': ['A user with that email already exists.']},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create user using allauth's adapter to ensure proper signal handling
            from allauth.account.utils import setup_user_email
            from allauth.account import app_settings as account_settings
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Set up email addresses and send confirmation
            setup_user_email(request, user, [])
            
            # Send email confirmation
            from allauth.account.utils import send_email_confirmation
            send_email_confirmation(request, user, email=email)
            
            logger.info(f"User registered successfully: {username}. Verification email sent.")
            
            return Response({
                'success': True,
                'message': 'Registration successful. Please check your email for verification instructions.',
                'username': user.username,
                'email': user.email,
                'email_verification_required': True
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.exception(f"Registration error: {str(e)}")
            return Response(
                {'non_field_errors': ['Registration failed. Please try again.']},
                status=status.HTTP_400_BAD_REQUEST
            )
@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')

        if not code:
            return Response({'non_field_errors': ['No authorization code provided']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token_response = requests.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'code': code,
                    'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
                    'client_secret': settings.GOOGLE_OAUTH2_SECRET,
                    'redirect_uri': 'postmessage',
                    'grant_type': 'authorization_code',
                }
            )

            if token_response.status_code != 200:
                return Response(
                    {'non_field_errors': ['Failed to exchange code']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token_data = token_response.json()
            access_token = token_data.get('access_token')

            user_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )

            if user_response.status_code != 200:
                return Response({'non_field_errors': ['Invalid Google token']}, status=status.HTTP_400_BAD_REQUEST)

            user_data = user_response.json()
            email = user_data.get('email')

            if not email:
                return Response({'non_field_errors': ['Email not provided by Google']}, status=status.HTTP_400_BAD_REQUEST)

            User = get_user_model()

            try:
                social_account = SocialAccount.objects.get(uid=user_data['sub'], provider='google')
                user = social_account.user
            except SocialAccount.DoesNotExist:
                try:
                    user = User.objects.get(email=email)
                except User.DoesNotExist:
                    user = User.objects.create_user(
                        username=email.split('@')[0],
                        email=email,
                        first_name=user_data.get('given_name', ''),
                        last_name=user_data.get('family_name', '')
                    )
                
                social_account = SocialAccount.objects.create(
                    user=user,
                    uid=user_data['sub'],
                    provider='google',
                    extra_data=user_data
                )

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            refresh = RefreshToken.for_user(user)

            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(f"Error in GoogleLoginView: {str(e)}")
            return Response({'non_field_errors': [str(e)]}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class GitHubLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get('code')
        redirect_uri = request.data.get('redirect_uri')

        if not code:
            logger.error("No authorization code provided for GitHub login")
            return Response({'non_field_errors': ['No authorization code provided']}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Validate redirect URI
        allowed_uris = settings.ALLOWED_GITHUB_REDIRECT_URIS if hasattr(settings, 'ALLOWED_GITHUB_REDIRECT_URIS') else []
        if redirect_uri not in allowed_uris:
            logger.error(f"Invalid redirect_uri: {redirect_uri}")
            return Response(
                {'non_field_errors': ['Invalid redirect URI']},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Exchange code for access token
            token_response = requests.post(
                'https://github.com/login/oauth/access_token',
                data={
                    'client_id': settings.GITHUB_OAUTH2_CLIENT_ID,
                    'client_secret': settings.GITHUB_OAUTH2_SECRET,
                    'code': code,
                    'redirect_uri': redirect_uri,
                },
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                timeout=30
            )

            if token_response.status_code != 200:
                logger.error(f"GitHub token exchange failed: {token_response.text}")
                return Response(
                    {'non_field_errors': ['Failed to exchange code for access token']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token_data = token_response.json()
            
            if 'error' in token_data:
                logger.error(f"GitHub OAuth error: {token_data['error']}")
                return Response(
                    {'non_field_errors': [f"GitHub authentication error: {token_data.get('error_description', token_data['error'])}"]},
                    status=status.HTTP_400_BAD_REQUEST
                )

            access_token = token_data.get('access_token')
            
            if not access_token:
                logger.error("No access token received from GitHub")
                return Response(
                    {'non_field_errors': ['No access token received from GitHub']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get user info with proper authentication
            user_response = requests.get(
                'https://api.github.com/user',
                headers={
                    'Authorization': f'token {access_token}',
                    'Accept': 'application/vnd.github.v3+json',
                },
                timeout=30
            )

            if user_response.status_code != 200:
                logger.error(f"Failed to get user info from GitHub: {user_response.text}")
                return Response(
                    {'non_field_errors': ['Failed to get user information from GitHub']},
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
                logger.error("No verified primary email found for GitHub user")
                return Response(
                    {'non_field_errors': ['No verified email address found. Please ensure your GitHub account has a verified email.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

            User = get_user_model()
            
            try:
                social_account = SocialAccount.objects.get(uid=user_data['id'], provider='github')
                user = social_account.user
            except SocialAccount.DoesNotExist:
                try:
                    user = User.objects.get(email=primary_email)
                except User.DoesNotExist:
                    username = user_data.get('login', primary_email.split('@')[0])
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
                
                social_account = SocialAccount.objects.create(
                    user=user,
                    uid=user_data['id'],
                    provider='github',
                    extra_data=user_data
                )

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            refresh = RefreshToken.for_user(user)

            logger.info(f"GitHub login successful for user: {user.username}")

            return Response({
                'token': str(refresh.access_token),
                'refresh': str(refresh),
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.exception(f"Network error during GitHub OAuth: {str(e)}")
            return Response(
                {'non_field_errors': ['Network error during authentication']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.exception(f"Unexpected error in GitHubLoginView: {str(e)}")
            return Response(
                {'non_field_errors': ['An unexpected error occurred during authentication']},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )            


urlpatterns = [
    path('', include('pages.urls', namespace='pages')),
    path('gpstest/', GpsTestView.as_view(), name='gpstest'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('accounts/', include('allauth.urls')),
    path('', lambda request: redirect('pages:index'), name='home'),
    path('api/auth/login/', CustomLoginView.as_view(), name='login'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    # path('api/auth/password/reset/', PasswordResetView.as_view(), name='api_password_reset'),
    # With this custom view:
    path('api/auth/password/reset/', CustomPasswordResetView.as_view(), name='api_password_reset'),
    path('api/auth/verify-email/<str:key>/', CustomConfirmEmailView.as_view(), name='verify_email'),
    path('api/auth/resend-verification/', ResendVerificationEmailView.as_view(), name='resend_verification'),
    
    # path('api/auth/password/reset/', 'accounts.views.CustomPasswordResetView.as_view()', name='api_password_reset'),
    path('api/auth/google/', GoogleLoginView.as_view(), name='google-login'),
    path('api/auth/github/', GitHubLoginView.as_view(), name='github-login'),
]