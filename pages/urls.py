from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('dashboard', views.index, name='dashboard'),
    path('profile', views.index, name='profile'),
    path('api_testing',views.api_testing, name ='api_testing'),
    path('FAQ',views.faq, name ='FAQ'),
]