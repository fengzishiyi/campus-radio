from django.contrib.auth.models import User
from django.db import models


class Album(models.Model):
    """专辑模型"""
    
    title = models.CharField('专辑标题', max_length=200)
    description = models.TextField('专辑描述', blank=True)
    cover_image_url = models.URLField('封面图链接', blank=True, help_text='外部图片链接')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums', verbose_name='创建者')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '专辑'
        verbose_name_plural = '专辑'
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def get_track_count(self):
        return self.tracks.count()


class AudioTrack(models.Model):
    """音频轨道模型"""
    
    SOURCE_CHOICES = [
        ('himalaya', '喜马拉雅'),
        ('netease', '网易云音乐'),
        ('qq', 'QQ音乐'),
        ('bilibili', 'B站'),
        ('youtube', 'YouTube'),
        ('other', '其他'),
    ]
    
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks', verbose_name='专辑')
    title = models.CharField('音频标题', max_length=200)
    audio_source = models.CharField('音频来源', max_length=20, choices=SOURCE_CHOICES)
    audio_url = models.URLField('音频链接', help_text='外部音频链接')
    duration = models.CharField('时长', max_length=20, blank=True, help_text='如：05:30')
    order = models.IntegerField('排序', default=0)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_tracks', verbose_name='上传者')
    uploaded_at = models.DateTimeField('上传时间', auto_now_add=True)
    play_count = models.IntegerField('播放次数', default=0)
    
    class Meta:
        verbose_name = '音频轨道'
        verbose_name_plural = '音频轨道'
        ordering = ['album', 'order']
        
    def __str__(self):
        return f"{self.album.title} - {self.title}"
    
    def increment_play_count(self):
        """增加播放计数"""
        self.play_count += 1
        self.save(update_fields=['play_count'])


class Script(models.Model):
    """文稿模型"""
    
    track = models.OneToOneField(AudioTrack, on_delete=models.CASCADE, related_name='script', verbose_name='音频轨道')
    title = models.CharField('文稿标题', max_length=200)
    content = models.TextField('文稿内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scripts', verbose_name='作者')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '文稿'
        verbose_name_plural = '文稿'
        
    def __str__(self):
        return f"{self.track.title} - 文稿"

