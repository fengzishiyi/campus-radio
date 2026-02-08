from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    """公告模型"""
    
    TYPE_CHOICES = [
        ('notice', '通知'),
        ('urgent', '紧急'),
        ('activity', '活动'),
        ('schedule_change', '排班变更'),
    ]
    
    DEPARTMENT_CHOICES = [
        ('all', '全部'),
        ('broadcast', '广播站'),
        ('himalaya', '喜马拉雅'),
    ]
    
    title = models.CharField('标题', max_length=200)
    content = models.TextField('内容')
    type = models.CharField('类型', max_length=20, choices=TYPE_CHOICES, default='notice')
    is_pinned = models.BooleanField('置顶', default=False)
    target_department = models.CharField('目标部门', max_length=20, choices=DEPARTMENT_CHOICES, default='all')
    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements', verbose_name='发布者')
    publish_time = models.DateTimeField('发布时间', auto_now_add=True)
    expire_time = models.DateTimeField('过期时间', null=True, blank=True)
    read_by = models.ManyToManyField(User, blank=True, related_name='read_announcements', verbose_name='已读用户')
    
    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        ordering = ['-is_pinned', '-publish_time']
        
    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"
    
    def is_expired(self):
        """检查是否已过期"""
        if self.expire_time:
            return timezone.now() > self.expire_time
        return False
    
    def is_unread_by(self, user):
        """检查用户是否未读"""
        return not self.read_by.filter(id=user.id).exists()

