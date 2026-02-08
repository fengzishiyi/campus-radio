from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class StudioBooking(models.Model):
    """录音室预约模型"""
    
    STATUS_CHOICES = [
        ('pending', '待确认'),
        ('confirmed', '已确认'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    ]
    
    date = models.DateField('预约日期')
    start_time = models.TimeField('开始时间')
    end_time = models.TimeField('结束时间')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name='预约人')
    purpose = models.CharField('用途说明', max_length=200)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '录音室预约'
        verbose_name_plural = '录音室预约'
        ordering = ['-date', 'start_time']
        
    def __str__(self):
        return f"{self.date} {self.start_time}-{self.end_time} - {self.user.profile.real_name}"
    
    def clean(self):
        """验证时间冲突"""
        if self.start_time >= self.end_time:
            raise ValidationError('结束时间必须晚于开始时间')
        
        # 检查同一天的其他预约是否有时间冲突（排除已取消和当前记录）
        conflicting_bookings = StudioBooking.objects.filter(
            date=self.date,
            status__in=['pending', 'confirmed', 'completed']
        ).exclude(pk=self.pk)
        
        for booking in conflicting_bookings:
            # 时间重叠条件：existing.start_time < new.end_time AND existing.end_time > new.start_time
            if booking.start_time < self.end_time and booking.end_time > self.start_time:
                raise ValidationError(
                    f'时间冲突：{booking.start_time}-{booking.end_time} 已被 {booking.user.profile.real_name} 预约'
                )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

