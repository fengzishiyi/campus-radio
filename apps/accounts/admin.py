from django.contrib import admin
from .models import UserProfile, InviteCode


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['real_name', 'user', 'student_id', 'department', 'role', 'created_at']
    list_filter = ['department', 'role', 'created_at']
    search_fields = ['real_name', 'student_id', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('用户信息', {
            'fields': ('user', 'real_name', 'student_id')
        }),
        ('联系方式', {
            'fields': ('phone', 'wechat')
        }),
        ('组织信息', {
            'fields': ('department', 'role')
        }),
        ('个人信息', {
            'fields': ('avatar', 'bio')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_used', 'created_by', 'created_at', 'used_by', 'used_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['code', 'created_by__username', 'used_by__username']
    readonly_fields = ['created_at', 'used_at']
    fieldsets = (
        ('邀请码信息', {
            'fields': ('code', 'is_used')
        }),
        ('创建信息', {
            'fields': ('created_by', 'created_at')
        }),
        ('使用信息', {
            'fields': ('used_by', 'used_at')
        }),
    )
