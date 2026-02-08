from django.contrib import admin
from .models import NewsItem


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ['date', 'title', 'reporter', 'created_at']
    list_filter = ['date', 'reporter', 'created_at']
    search_fields = ['title', 'script_text', 'reporter__username', 'reporter__profile__real_name']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('date', 'title', 'reporter')
        }),
        ('内容', {
            'fields': ('audio_url', 'script_text')
        }),
        ('元数据', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
