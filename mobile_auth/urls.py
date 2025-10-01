# mobile_auth/urls.py
# Dedicated URL configurations for mobile authentication endpoints
# REST API focused, separate from web auth in accounts app

from django.urls import path
from . import views

app_name = 'mobile_auth'

urlpatterns = [
    path('login/', views.MobileLoginView.as_view(), name='mobile_login'),
    path('register/', views.MobileRegisterView.as_view(), name='mobile_register'),
    path('google/', views.MobileGoogleLoginView.as_view(), name='mobile_google_login'),
    path('github/', views.MobileGitHubLoginView.as_view(), name='mobile_github_login'),
    
    # Password reset endpoints
    path('password/reset/', views.MobilePasswordResetView.as_view(), name='mobile_password_reset'),
    path('password/reset/confirm/', views.MobilePasswordResetConfirmView.as_view(), name='mobile_password_reset_confirm'),
    path('password/change/', views.MobilePasswordChangeView.as_view(), name='mobile_password_change'),
]