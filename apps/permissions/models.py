from django.db import models


class ModulePermission(models.Model):
    """板块权限模型"""
    
    module_name = models.CharField('模块标识', max_length=50, unique=True)
    module_label = models.CharField('模块名称', max_length=100)
    allowed_roles = models.JSONField('允许的角色', default=list, help_text='角色列表，如 ["admin", "anchor"]')
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '板块权限'
        verbose_name_plural = '板块权限'
        ordering = ['module_name']
        
    def __str__(self):
        return f"{self.module_label} ({self.module_name})"
    
    def can_edit(self, user):
        """检查用户是否有编辑权限"""
        if not hasattr(user, 'profile'):
            return False
        return user.profile.role in self.allowed_roles

