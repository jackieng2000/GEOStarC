# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'profile.html')

def custom_logout(request):
    """Custom logout function"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')