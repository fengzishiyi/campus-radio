from django.contrib import admin
from .models import ModulePermission


class ModulePermissionAdmin(admin.ModelAdmin):
    list_display = ('module_name', 'module_label', 'allowed_roles', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('module_name', 'module_label')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(ModulePermission, ModulePermissionAdmin)
