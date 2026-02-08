from django.contrib import admin
from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'is_pinned', 'target_department', 'publisher', 'publish_time', 'expire_time', 'read_count']
    list_filter = ['type', 'is_pinned', 'target_department', 'publish_time']
    search_fields = ['title', 'content', 'publisher__username', 'publisher__first_name', 'publisher__last_name']
    readonly_fields = ['publish_time', 'read_count']
    filter_horizontal = ['read_by']
    date_hierarchy = 'publish_time'
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'content', 'type', 'publisher')
        }),
        ('发布设置', {
            'fields': ('is_pinned', 'target_department', 'expire_time')
        }),
        ('统计信息', {
            'fields': ('publish_time', 'read_count', 'read_by'),
            'classes': ('collapse',)
        }),
    )
    
    def read_count(self, obj):
        return obj.read_by.count()
    read_count.short_description = '已读人数'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.publisher = request.user
        super().save_model(request, obj, form, change)
