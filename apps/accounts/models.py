from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """用户资料模型"""
    
    DEPARTMENT_CHOICES = [
        ('broadcast', '广播站'),
        ('himalaya', '喜马拉雅'),
        ('both', '两者兼任'),
    ]
    
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('anchor', '播音员'),
        ('himalaya', '喜马拉雅人员'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    real_name = models.CharField('姓名', max_length=50)
    student_id = models.CharField('学号', max_length=20, unique=True)
    phone = models.CharField('手机号', max_length=20, blank=True)
    wechat = models.CharField('微信号', max_length=50, blank=True)
    department = models.CharField('所属部门', max_length=20, choices=DEPARTMENT_CHOICES)
    role = models.CharField('角色', max_length=20, choices=ROLE_CHOICES)
    avatar = models.ImageField('头像', upload_to='avatars/', blank=True, null=True)
    bio = models.TextField('个人简介', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
        
    def __str__(self):
        return f"{self.real_name} ({self.get_role_display()})"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_anchor(self):
        return self.role == 'anchor'
    
    def is_himalaya(self):
        return self.role == 'himalaya'


class InviteCode(models.Model):
    """邀请码模型"""
    
    code = models.CharField('邀请码', max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_codes', verbose_name='创建者')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    used_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='used_code', verbose_name='使用者')
    used_at = models.DateTimeField('使用时间', null=True, blank=True)
    is_used = models.BooleanField('已使用', default=False)
    
    class Meta:
        verbose_name = '邀请码'
        verbose_name_plural = '邀请码'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.code} ({'已使用' if self.is_used else '未使用'})"

