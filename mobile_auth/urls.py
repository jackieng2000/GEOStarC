# mobile_auth/urls.py
from django.urls import path
from . import views

app_name = 'mobile_auth'

urlpatterns = [
    path('login/', views.MobileLoginView.as_view(), name='mobile_login'),
    path('register/', views.MobileRegisterView.as_view(), name='mobile_register'),
    path('google/', views.MobileGoogleLoginView.as_view(), name='mobile_google_login'),
    path('github/', views.MobileGitHubLoginView.as_view(), name='mobile_github_login'),
]