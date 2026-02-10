from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    """广播站分组模型"""
    
    WEEKDAY_CHOICES = [
        (1, '周一'),
        (2, '周二'),
        (3, '周三'),
        (4, '周四'),
        (5, '周五'),
        (7, '周日'),
    ]
    
    name = models.CharField('组名', max_length=50)
    weekday = models.IntegerField('对应星期', choices=WEEKDAY_CHOICES, unique=True)
    leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_groups', verbose_name='组长')
    members = models.ManyToManyField(User, blank=True, related_name='broadcast_groups', verbose_name='组员')
    
    class Meta:
        verbose_name = '分组'
        verbose_name_plural = '分组'
        ordering = ['weekday']
        
    def __str__(self):
        return f"{self.name} ({self.get_weekday_display()})"


class DailySchedule(models.Model):
    """日程安排模型"""
    
    date = models.DateField('日期', unique=True)
    anchors = models.ManyToManyField(User, blank=True, related_name='daily_schedules', verbose_name='播音员')
    is_live = models.BooleanField('是否直播', default=False, help_text='16:00-18:00直播标记')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_schedules', verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '日程安排'
        verbose_name_plural = '日程安排'
        ordering = ['-date']
        
    def __str__(self):
        return f"{self.date} 的排班"


class Program(models.Model):
    """节目模型"""
    
    schedule = models.ForeignKey(DailySchedule, on_delete=models.CASCADE, related_name='programs', verbose_name='日程')
    name = models.CharField('节目名称', max_length=100)
    time_slot = models.CharField('时间段', max_length=50)
    order = models.IntegerField('排序', default=0)
    
    class Meta:
        verbose_name = '节目'
        verbose_name_plural = '节目'
        ordering = ['order', 'time_slot']
        
    def __str__(self):
        return f"{self.name} ({self.time_slot})"


class Song(models.Model):
    """歌曲模型"""
    
    schedule = models.ForeignKey(DailySchedule, on_delete=models.CASCADE, related_name='songs', verbose_name='日程')
    title = models.CharField('歌曲名', max_length=100)
    artist = models.CharField('歌手', max_length=100, blank=True)
    audio_file = models.FileField('音频文件', upload_to='daily_songs/%Y/%m/%d/', blank=True, null=True, help_text='上传的MP3等音频文件')
    order = models.IntegerField('排序', default=0)
    
    class Meta:
        verbose_name = '歌曲'
        verbose_name_plural = '歌曲'
        ordering = ['order', 'title']
        
    def __str__(self):
        if self.artist:
            return f"{self.title} - {self.artist}"
        return self.title

