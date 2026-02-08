from django import forms
from .models import NewsItem


class NewsItemForm(forms.ModelForm):
    """新闻项目表单"""
    
    class Meta:
        model = NewsItem
        fields = ['date', 'title', 'audio_url', 'script_text']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '输入新闻标题'
            }),
            'audio_url': forms.URLInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': 'https://example.com/audio.mp3'
            }),
            'script_text': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 10,
                'placeholder': '输入新闻文稿内容'
            }),
        }
