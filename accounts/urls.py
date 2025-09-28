
from django.urls import path, include
from . import views
from . import social_views
from .views import EmailConfHelpView

from accounts.views import EnsureCSRFTokenView

app_name = 'accounts'

urlpatterns = [
    
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    
    
    path('registration-info/', views.registration_info, name='registration_info'),
    path('email-confirmation-help/', EmailConfHelpView.as_view(), 
         name='email_conf_help'),
     path('api/csrf-token/', EnsureCSRFTokenView.as_view(), name='csrf_token'),
    
    path('api/google-login/', social_views.google_login, name='google_login'),
    path('api/google-auth-url/', social_views.google_auth_url, name='google_auth_url'),
    path('api/github-login/', social_views.github_login, name='github_login'),
    path('api/github-auth-url/', social_views.github_auth_url, name='github_auth_url'),
    
    # Include allauth URLs - IMPORTANT!
  
]