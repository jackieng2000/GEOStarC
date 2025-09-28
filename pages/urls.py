from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('dashboard', views.index, name='dashboard'),
    path('profile', views.index, name='profile'),
    path('about',views.about, name ='about'),
    path('FAQ',views.faq, name ='FAQ'),
]