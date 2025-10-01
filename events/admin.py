# events/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Event, EventAdmin, EventUser

@admin.register(Event)
class EventAdminPanel(admin.ModelAdmin):
    list_display = [
        'EventName', 
        'get_event_type', 
        'AdminUser', 
        'get_enrollment_status', 
        'get_event_status', 
        'get_start_time',
        'CreateTimeStamp'
    ]
    
    list_filter = [
        'Type', 
        'Active', 
        'CreateTimeStamp', 
        'StartTimestamp',
        'Country'
    ]
    
    search_fields = [
        'EventName', 
        'Description', 
        'Country',
        'Location',
        'AdminUser__username',
        'AdminUser__email'
    ]
    
    readonly_fields = [
        'CreateTimeStamp', 
        'Enrolled',
        'get_event_status_display',
        'get_duration_display'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'EventName', 
                'Description', 
                'Type', 
                'AdminUser'
            )
        }),
        ('Event Details', {
            'fields': (
                'StartTimestamp', 
                'EndTimestamp', 
                'Distance', 
                'Elevation',
                'get_duration_display'
            )
        }),
        ('Location', {
            'fields': (
                'Country', 
                'Location'
            )
        }),
        ('Files & Limits', {
            'fields': (
                'GpxFile', 
                'MaxParticipants'
            )
        }),
        ('Status', {
            'fields': (
                'Active', 
                'CreateTimeStamp', 
                'Enrolled',
                'get_event_status_display'
            )
        }),
    )
    
    filter_horizontal = ()
    date_hierarchy = 'StartTimestamp'
    ordering = ['-CreateTimeStamp']
    list_per_page = 25
    
    # Custom methods for list display
    def get_event_type(self, obj):
        color_map = {
            'T': 'orange',
            'R': 'red', 
            'C': 'green'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color_map.get(obj.Type, 'black'),
            obj.get_Type_display()
        )
    get_event_type.short_description = 'Type'
    get_event_type.admin_order_field = 'Type'
    
    def get_enrollment_status(self, obj):
        if obj.MaxParticipants:
            percentage = (obj.Enrolled / obj.MaxParticipants) * 100
            color = 'green' if percentage < 80 else 'orange' if percentage < 100 else 'red'
            return format_html(
                '<span style="color: {};">{}/{} ({:.1f}%)</span>',
                color, obj.Enrolled, obj.MaxParticipants, percentage
            )
        return f"{obj.Enrolled} enrolled"
    get_enrollment_status.short_description = 'Enrollment'
    get_enrollment_status.admin_order_field = 'Enrolled'
    
    def get_event_status(self, obj):
        now = timezone.now()
        
        if obj.is_upcoming():
            return format_html(
                '<span style="color: blue; font-weight: bold;">⏰ Upcoming</span>'
            )
        elif obj.is_ongoing():
            return format_html(
                '<span style="color: green; font-weight: bold;">▶️ Ongoing</span>'
            )
        elif obj.is_past():
            return format_html(
                '<span style="color: gray; font-weight: bold;">✅ Past</span>'
            )
        else:
            status = 'Active' if obj.Active else 'Inactive'
            color = 'green' if obj.Active else 'gray'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color, status
            )
    get_event_status.short_description = 'Status'
    
    def get_start_time(self, obj):
        if obj.StartTimestamp:
            return obj.StartTimestamp.strftime('%Y-%m-%d %H:%M')
        return 'Not set'
    get_start_time.short_description = 'Start Time'
    get_start_time.admin_order_field = 'StartTimestamp'
    
    # Custom methods for readonly fields
    def get_event_status_display(self, obj):
        return self.get_event_status(obj)
    get_event_status_display.short_description = 'Current Status'
    
    def get_duration_display(self, obj):
        duration = obj.get_duration()
        if duration:
            return f"{duration} hours"
        return "Not set"
    get_duration_display.short_description = 'Duration'
    
    # Actions
    actions = ['activate_events', 'deactivate_events', 'mark_as_trail', 'mark_as_race', 'mark_as_casual']
    
    def activate_events(self, request, queryset):
        updated = queryset.update(Active=True)
        self.message_user(request, f'{updated} events activated successfully.')
    activate_events.short_description = "Activate selected events"
    
    def deactivate_events(self, request, queryset):
        updated = queryset.update(Active=False)
        self.message_user(request, f'{updated} events deactivated successfully.')
    deactivate_events.short_description = "Deactivate selected events"
    
    def mark_as_trail(self, request, queryset):
        updated = queryset.update(Type='T')
        self.message_user(request, f'{updated} events marked as Trail.')
    mark_as_trail.short_description = "Mark selected as Trail"
    
    def mark_as_race(self, request, queryset):
        updated = queryset.update(Type='R')
        self.message_user(request, f'{updated} events marked as Race.')
    mark_as_race.short_description = "Mark selected as Race"
    
    def mark_as_casual(self, request, queryset):
        updated = queryset.update(Type='C')
        self.message_user(request, f'{updated} events marked as Casual.')
    mark_as_casual.short_description = "Mark selected as Casual"


@admin.register(EventAdmin)
class EventAdministratorAdmin(admin.ModelAdmin):
    list_display = [
        'get_event_name',
        'get_username',
        'get_email',
        'Role',
        'AssignedTimestamp',
        'get_event_type'
    ]
    
    list_filter = [
        'AssignedTimestamp',
        'Role',
        'EventId__Type',
        'EventId__Active'
    ]
    
    search_fields = [
        'EventId__EventName',
        'UserId__username',
        'UserId__email',
        'Role'
    ]
    
    readonly_fields = [
        'AssignedTimestamp'
    ]
    
    fieldsets = (
        ('Event Information', {
            'fields': ('EventId',)
        }),
        ('Administrator Information', {
            'fields': ('UserId', 'Role')
        }),
        ('Metadata', {
            'fields': ('AssignedTimestamp',)
        }),
    )
    
    autocomplete_fields = ['EventId', 'UserId']
    list_per_page = 25
    
    # Custom methods for list display
    def get_event_name(self, obj):
        return obj.EventId.EventName
    get_event_name.short_description = 'Event Name'
    get_event_name.admin_order_field = 'EventId__EventName'
    
    def get_username(self, obj):
        return obj.UserId.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'UserId__username'
    
    def get_email(self, obj):
        return obj.UserId.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'UserId__email'
    
    def get_event_type(self, obj):
        return obj.EventId.get_Type_display()
    get_event_type.short_description = 'Event Type'
    get_event_type.admin_order_field = 'EventId__Type'


@admin.register(EventUser)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = [
        'get_event_name',
        'get_username',
        'get_email',
        'get_completion_status',
        'get_start_time',
        'get_end_time',
        'get_net_time',
        'EnrolledTimestamp'
    ]
    
    list_filter = [
        'Completed',
        'EnrolledTimestamp',
        'StartTimestamp',
        'EndTimestamp',
        'EventId__Type',
        'EventId__Active'
    ]
    
    search_fields = [
        'EventId__EventName',
        'UserId__username',
        'UserId__email',
        'Notes'
    ]
    
    readonly_fields = [
        'EnrolledTimestamp',
        'NetTime',
        'get_participation_status'
    ]
    
    fieldsets = (
        ('Event Information', {
            'fields': ('EventId',)
        }),
        ('Participant Information', {
            'fields': ('UserId',)
        }),
        ('Participation Details', {
            'fields': (
                'StartTimestamp',
                'EndTimestamp',
                'NetTime',
                'Completed',
                'DistanceCompleted',
                'get_participation_status'
            )
        }),
        ('Additional Information', {
            'fields': ('Notes', 'EnrolledTimestamp')
        }),
    )
    
    autocomplete_fields = ['EventId', 'UserId']
    date_hierarchy = 'EnrolledTimestamp'
    list_per_page = 25
    
    # Custom methods for list display
    def get_event_name(self, obj):
        return obj.EventId.EventName
    get_event_name.short_description = 'Event Name'
    get_event_name.admin_order_field = 'EventId__EventName'
    
    def get_username(self, obj):
        return obj.UserId.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'UserId__username'
    
    def get_email(self, obj):
        return obj.UserId.email
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'UserId__email'
    
    def get_completion_status(self, obj):
        if obj.Completed:
            return format_html(
                '<span style="color: green; font-weight: bold;">✅ Completed</span>'
            )
        elif obj.is_active_participant():
            return format_html(
                '<span style="color: orange; font-weight: bold;">▶️ In Progress</span>'
            )
        else:
            return format_html(
                '<span style="color: blue; font-weight: bold;">⏰ Registered</span>'
            )
    get_completion_status.short_description = 'Status'
    
    def get_start_time(self, obj):
        if obj.StartTimestamp:
            return obj.StartTimestamp.strftime('%Y-%m-%d %H:%M')
        return 'Not started'
    get_start_time.short_description = 'Start Time'
    get_start_time.admin_order_field = 'StartTimestamp'
    
    def get_end_time(self, obj):
        if obj.EndTimestamp:
            return obj.EndTimestamp.strftime('%Y-%m-%d %H:%M')
        return 'Not finished'
    get_end_time.short_description = 'End Time'
    get_end_time.admin_order_field = 'EndTimestamp'
    
    def get_net_time(self, obj):
        if obj.NetTime:
            # Format duration as HH:MM:SS
            total_seconds = int(obj.NetTime.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return 'N/A'
    get_net_time.short_description = 'Net Time'
    get_net_time.admin_order_field = 'NetTime'
    
    # Custom methods for readonly fields
    def get_participation_status(self, obj):
        return self.get_completion_status(obj)
    get_participation_status.short_description = 'Participation Status'
    
    # Actions
    actions = ['mark_as_completed', 'mark_as_in_progress', 'reset_participation']
    
    def mark_as_completed(self, request, queryset):
        for participant in queryset:
            if participant.StartTimestamp and not participant.EndTimestamp:
                participant.EndTimestamp = timezone.now()
                participant.calculate_net_time()
                participant.Completed = True
                participant.save()
        self.message_user(request, f'Selected participants marked as completed.')
    mark_as_completed.short_description = "Mark selected as completed"
    
    def mark_as_in_progress(self, request, queryset):
        updated = queryset.filter(StartTimestamp__isnull=True).update(StartTimestamp=timezone.now())
        self.message_user(request, f'{updated} participants marked as in progress.')
    mark_as_in_progress.short_description = "Mark selected as in progress"
    
    def reset_participation(self, request, queryset):
        updated = queryset.update(
            StartTimestamp=None,
            EndTimestamp=None,
            NetTime=None,
            Completed=False,
            DistanceCompleted=0.00
        )
        self.message_user(request, f'{updated} participants reset.')
    reset_participation.short_description = "Reset participation data"


# Optional: Custom admin site header and title
admin.site.site_header = "GEOStar Events Administration"
admin.site.site_title = "GEOStar Events Admin"
admin.site.index_title = "Event Management"