from django.shortcuts import render, get_object_or_404
from django.urls import path
from . import views

# views.py

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

@method_decorator(csrf_exempt, name='dispatch')
class GpsTestView(View):
    def get(self, request):
        # Allow both authenticated and unauthenticated access
        return render(request, 'pages/gpstest.html')


def index(request):
    
    context = {}
    return render(request, 'pages/index.html')

def dashboard(request):
    
    context = {}
    return render(request, 'pages/index.html')

def profile(request):
    
    context = {}
    return render(request, 'pages/index.html')

def about(request):
    
    context = {}
    return render(request, 'pages/index.html')

def faq(request):
    
    context = {}
    return render(request, 'pages/index.html')