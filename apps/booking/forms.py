from django import forms
from django.core.exceptions import ValidationError
from .models import StudioBooking


class StudioBookingForm(forms.ModelForm):
    """录音室预约表单"""
    
    class Meta:
        model = StudioBooking
        fields = ['date', 'start_time', 'end_time', 'purpose']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'purpose': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '请输入预约用途说明'
            })
        }
        labels = {
            'date': '预约日期',
            'start_time': '开始时间',
            'end_time': '结束时间',
            'purpose': '用途说明'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise ValidationError('结束时间必须晚于开始时间')
        
        return cleaned_data
