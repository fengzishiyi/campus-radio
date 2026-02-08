from django import forms
from django.contrib.auth.models import User
from .models import Group, DailySchedule, Program, Song


class GroupForm(forms.ModelForm):
    """Form for editing group leader and members"""
    
    class Meta:
        model = Group
        fields = ['leader', 'members']
        widgets = {
            'leader': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'members': forms.SelectMultiple(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'size': '8'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['leader'].queryset = User.objects.filter(is_active=True).order_by('profile__real_name')
        self.fields['leader'].label_from_instance = lambda obj: obj.profile.real_name if hasattr(obj, 'profile') else obj.username
        self.fields['members'].queryset = User.objects.filter(is_active=True).order_by('profile__real_name')
        self.fields['members'].label_from_instance = lambda obj: obj.profile.real_name if hasattr(obj, 'profile') else obj.username


class DailyScheduleForm(forms.ModelForm):
    """Form for selecting anchors for a day"""
    
    class Meta:
        model = DailySchedule
        fields = ['anchors']
        widgets = {
            'anchors': forms.SelectMultiple(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'size': '6'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anchors'].queryset = User.objects.filter(is_active=True).order_by('profile__real_name')
        self.fields['anchors'].label_from_instance = lambda obj: obj.profile.real_name if hasattr(obj, 'profile') else obj.username
        self.fields['anchors'].required = False


class ProgramForm(forms.ModelForm):
    """Form for adding/editing a program"""
    
    class Meta:
        model = Program
        fields = ['name', 'time_slot', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '节目名称'
            }),
            'time_slot': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '例如: 12:00-12:30'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'value': '0'
            }),
        }


class SongForm(forms.ModelForm):
    """Form for adding/editing a song"""
    
    class Meta:
        model = Song
        fields = ['title', 'artist', 'order']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '歌曲名'
            }),
            'artist': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': '歌手 (可选)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'value': '0'
            }),
        }
