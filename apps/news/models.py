from django.contrib.auth.models import User
from django.db import models


class NewsItem(models.Model):
    """新闻项目模型"""
    
    date = models.DateField('播报日期')
    title = models.CharField('新闻标题', max_length=200)
    audio_url = models.URLField('音频链接', blank=True, help_text='外部音频链接（喜马拉雅/网易云/QQ音乐/B站等）')
    script_text = models.TextField('新闻文稿', blank=True)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news_items', verbose_name='播报员/上传人')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    
    class Meta:
        verbose_name = '新闻项目'
        verbose_name_plural = '新闻项目'
        ordering = ['-date', '-created_at']
        
    def __str__(self):
        return f"{self.date} - {self.title}"

