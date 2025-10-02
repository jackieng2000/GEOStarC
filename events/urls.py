# events/urls.py
from django.urls import path
from .views.event_views import (  # 🆕 All imports from event_views
    event_maintenance,
    manage_event_admins, 
    remove_event_admin,
    manage_event_users,
    update_event_user,
    remove_event_user
)

app_name = 'events'

urlpatterns = [
    path('maintenance/', event_maintenance, name='event_maintenance'),
    path('maintenance/<int:event_id>/', event_maintenance, name='event_maintenance_with_id'),
    path('<int:event_id>/admins/', manage_event_admins, name='manage_event_admins'),
    path('<int:event_id>/admins/remove/<int:admin_id>/', remove_event_admin, name='remove_event_admin'),
    path('<int:event_id>/users/', manage_event_users, name='manage_event_users'),
    path('<int:event_id>/users/update/<int:event_user_id>/', update_event_user, name='update_event_user'),
    path('<int:event_id>/users/remove/<int:event_user_id>/', remove_event_user, name='remove_event_user'),
]