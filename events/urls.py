# events/urls.py
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('maintenance/', views.event_maintenance, name='event_maintenance'),
    path('maintenance/<int:event_id>/', views.event_maintenance, name='event_maintenance_with_id'),
    path('<int:event_id>/admins/', views.manage_event_admins, name='manage_event_admins'),
    path('<int:event_id>/admins/remove/<int:admin_id>/', views.remove_event_admin, name='remove_event_admin'),
    path('<int:event_id>/users/', views.manage_event_users, name='manage_event_users'),
    path('<int:event_id>/users/update/<int:event_user_id>/', views.update_event_user, name='update_event_user'),
    path('<int:event_id>/users/remove/<int:event_user_id>/', views.remove_event_user, name='remove_event_user'),
]