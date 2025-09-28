# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('logout/', views.custom_logout, name='custom_logout'),
]