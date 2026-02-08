from django.contrib import admin
from .models import StudioBooking


@admin.register(StudioBooking)
class StudioBookingAdmin(admin.ModelAdmin):
    list_display = ['date', 'start_time', 'end_time', 'user', 'purpose', 'status', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['user__username', 'user__profile__real_name', 'purpose']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('date', 'start_time', 'end_time', 'user', 'purpose')
        }),
        ('状态', {
            'fields': ('status',)
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
