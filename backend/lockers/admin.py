from django.contrib import admin
from .models import Locker


@admin.register(Locker)
class LockerAdmin(admin.ModelAdmin):
    list_display = ['locker_number', 'status', 'rented_by', 'rental_hours', 'is_active', 'created_at']
    list_filter = ['status', 'is_active', 'created_at']
    search_fields = ['locker_number', 'rented_by__username']
    readonly_fields = ['created_at', 'updated_at', 'id']
    fieldsets = (
        ('Locker Information', {
            'fields': ('id', 'locker_number', 'is_active')
        }),
        ('Status', {
            'fields': ('status', 'rented_by', 'rental_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ['locker_number']