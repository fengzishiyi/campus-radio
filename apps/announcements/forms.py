from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    """Form for creating and editing announcements"""
    
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'type', 'is_pinned', 'target_department', 'expire_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '输入公告标题'
            }),
            'content': forms.Textarea(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'rows': 6,
                'placeholder': '输入公告内容'
            }),
            'type': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'is_pinned': forms.CheckboxInput(attrs={
                'class': 'rounded border-gray-300 text-blue-600 focus:ring-blue-500'
            }),
            'target_department': forms.Select(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'expire_time': forms.DateTimeInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'type': 'datetime-local',
                'placeholder': '可选，留空表示永不过期'
            }),
        }
        labels = {
            'title': '标题',
            'content': '内容',
            'type': '类型',
            'is_pinned': '置顶',
            'target_department': '目标部门',
            'expire_time': '过期时间',
        }
        help_texts = {
            'expire_time': '留空表示永不过期',
            'is_pinned': '置顶的公告会显示在列表顶部',
        }
