# events/views/event_views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db import transaction
from django.core.exceptions import PermissionDenied
from ..models import Event, EventAdmin, EventUser
from ..forms import EventAdminForm, EventUserForm, EventForm

# events/views.py - Update the event_maintenance function
@login_required
def event_maintenance(request, event_id=None):
    """
    Main event maintenance page - allows creating new events or selecting existing ones
    """
    events = Event.objects.filter(AdminUser=request.user)
    event = None
    event_form = None
    
    # Handle event creation
    if request.method == 'POST' and 'create_event' in request.POST:
        event_form = EventForm(request.POST)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.AdminUser = request.user
            new_event.save()
            messages.success(request, f'Event "{new_event.EventName}" created successfully!')
            return redirect('events:event_maintenance_with_id', event_id=new_event.EventId)
    
    # Handle event update
    elif request.method == 'POST' and 'update_event' in request.POST and event_id:
        event = get_object_or_404(Event, EventId=event_id, AdminUser=request.user)
        event_form = EventForm(request.POST, instance=event)
        if event_form.is_valid():
            updated_event = event_form.save()
            messages.success(request, f'Event "{updated_event.EventName}" updated successfully!')
            return redirect('events:event_maintenance_with_id', event_id=event_id)
    else:
        event_form = EventForm()
    
    if event_id:
        event = get_object_or_404(Event, EventId=event_id, AdminUser=request.user)
        # Pre-populate the form with existing event data for editing
        event_form = EventForm(instance=event)
    
    context = {
        'events': events,
        'selected_event': event,
        'event_form': event_form,
    }
    return render(request, 'events/event_maintenance.html', context)


@login_required
def manage_event_admins(request, event_id):
    """
    Manage additional administrators for an event
    """
    event = get_object_or_404(Event, EventId=event_id)
    
    # Check if user is event admin
    if not (event.AdminUser == request.user or 
            EventAdmin.objects.filter(EventId=event, UserId=request.user).exists()):
        raise PermissionDenied("You don't have permission to manage this event's administrators.")
    
    event_admins = EventAdmin.objects.filter(EventId=event)
    
    if request.method == 'POST':
        form = EventAdminForm(request.POST, event=event)
        if form.is_valid():
            event_admin = form.save(commit=False)
            event_admin.EventId = event
            event_admin.save()
            
            messages.success(request, f'{event_admin.UserId.username} has been added as an event administrator.')
            return redirect('events:manage_event_admins', event_id=event_id)
    else:
        form = EventAdminForm(event=event)
    
    context = {
        'event': event,
        'event_admins': event_admins,
        'form': form,
    }
    return render(request, 'events/manage_event_admins.html', context)

@login_required
def remove_event_admin(request, event_id, admin_id):
    """
    Remove an event administrator
    """
    event = get_object_or_404(Event, EventId=event_id)
    
    # Check if user is event admin
    if not (event.AdminUser == request.user or 
            EventAdmin.objects.filter(EventId=event, UserId=request.user).exists()):
        raise PermissionDenied("You don't have permission to manage this event's administrators.")
    
    event_admin = get_object_or_404(EventAdmin, id=admin_id, EventId=event)
    
    # Prevent removing the main admin user
    if event_admin.UserId == event.AdminUser:
        messages.error(request, "Cannot remove the main event administrator.")
        return redirect('events:manage_event_admins', event_id=event_id)
    
    if request.method == 'POST':
        username = event_admin.UserId.username
        event_admin.delete()
        messages.success(request, f'{username} has been removed as an event administrator.')
        return redirect('events:manage_event_admins', event_id=event_id)
    
    context = {
        'event': event,
        'event_admin': event_admin,
    }
    return render(request, 'events/remove_event_admin.html', context)

@login_required
def manage_event_users(request, event_id):
    """
    Manage event participants (users enrolled in the event)
    """
    event = get_object_or_404(Event, EventId=event_id)
    
    # Check if user is event admin
    if not (event.AdminUser == request.user or 
            EventAdmin.objects.filter(EventId=event, UserId=request.user).exists()):
        raise PermissionDenied("You don't have permission to manage this event's participants.")
    
    event_users = EventUser.objects.filter(EventId=event).select_related('UserId')
    
    if request.method == 'POST':
        form = EventUserForm(request.POST, event=event)
        if form.is_valid():
            event_user = form.save(commit=False)
            event_user.EventId = event
            
            # Check if user is already enrolled
            if EventUser.objects.filter(EventId=event, UserId=event_user.UserId).exists():
                messages.error(request, f'User {event_user.UserId.username} is already enrolled in this event.')
            else:
                event_user.save()
                messages.success(request, f'{event_user.UserId.username} has been enrolled in the event.')
                return redirect('events:manage_event_users', event_id=event_id)
    else:
        form = EventUserForm(event=event)
    
    context = {
        'event': event,
        'event_users': event_users,
        'form': form,
    }
    return render(request, 'events/manage_event_users.html', context)

@login_required
def update_event_user(request, event_id, event_user_id):
    """
    Update event user participation details
    """
    event = get_object_or_404(Event, EventId=event_id)
    event_user = get_object_or_404(EventUser, id=event_user_id, EventId=event)
    
    # Check if user is event admin
    if not (event.AdminUser == request.user or 
            EventAdmin.objects.filter(EventId=event, UserId=request.user).exists()):
        raise PermissionDenied("You don't have permission to manage this event's participants.")
    
    if request.method == 'POST':
        form = EventUserForm(request.POST, instance=event_user, event=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Participation details for {event_user.UserId.username} have been updated.')
            return redirect('events:manage_event_users', event_id=event_id)
    else:
        form = EventUserForm(instance=event_user, event=event)
    
    context = {
        'event': event,
        'event_user': event_user,
        'form': form,
    }
    return render(request, 'events/update_event_user.html', context)

@login_required
def remove_event_user(request, event_id, event_user_id):
    """
    Remove a user from the event
    """
    event = get_object_or_404(Event, EventId=event_id)
    event_user = get_object_or_404(EventUser, id=event_user_id, EventId=event)
    
    # Check if user is event admin
    if not (event.AdminUser == request.user or 
            EventAdmin.objects.filter(EventId=event, UserId=request.user).exists()):
        raise PermissionDenied("You don't have permission to manage this event's participants.")
    
    if request.method == 'POST':
        username = event_user.UserId.username
        event_user.delete()
        messages.success(request, f'{username} has been removed from the event.')
        return redirect('events:manage_event_users', event_id=event_id)
    
    context = {
        'event': event,
        'event_user': event_user,
    }
    return render(request, 'events/remove_event_user.html', context)