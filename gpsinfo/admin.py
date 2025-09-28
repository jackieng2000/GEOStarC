# gpsinfo/admin.py
from django.contrib import admin
from .models import GPSLocation, GPSLatest
from django.utils import timezone

@admin.register(GPSLatest)
class GPSLatestAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'latitude', 'longitude', 'formatted_timestamp', 'altitude', 'accuracy')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

    def get_username(self, obj):
        return obj.user.username if obj.user else "Unknown"
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'

    def formatted_timestamp(self, obj):
        if obj.timestamp:
            return timezone.localtime(obj.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return "No timestamp"
    formatted_timestamp.short_description = 'Timestamp'

@admin.register(GPSLocation)
class GPSLocationAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'formatted_timestamp', 'latitude', 'longitude', 'altitude', 'accuracy')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

    def get_username(self, obj):
        return obj.user.username if obj.user else "Unknown"
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'

    def formatted_timestamp(self, obj):
        if obj.timestamp:
            return timezone.localtime(obj.timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return "No timestamp"
    formatted_timestamp.short_description = 'Timestamp'
    formatted_timestamp.admin_order_field = 'timestamp'