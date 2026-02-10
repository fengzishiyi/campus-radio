from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from .models import StudioBooking


class StudioBookingForm(forms.ModelForm):
    """录音室预约表单"""
    
    TIME_SLOT_CHOICES = [
        ('08:00-10:00', '上午 8:00-10:00'),
        ('10:00-12:00', '上午 10:00-12:00'),
        ('14:00-16:00', '下午 14:00-16:00'),
        ('16:00-18:00', '下午 16:00-18:00'),
        ('19:00-21:00', '晚上 19:00-21:00'),
        ('21:00-22:00', '晚上 21:00-22:00'),
    ]
    
    time_slot = forms.ChoiceField(
        label='预约时间段',
        choices=TIME_SLOT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
        })
    )
    
    class Meta:
        model = StudioBooking
        fields = ['date', 'purpose']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'
            }),
            'purpose': forms.TextInput(attrs={
                'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500',
                'placeholder': '请输入预约用途说明'
            })
        }
        labels = {
            'date': '预约日期',
            'purpose': '用途说明'
        }
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        slot = cleaned_data.get('time_slot')
        
        if date and slot:
            # Parse time slot to get start and end times
            start_str, end_str = slot.split('-')
            start_time = datetime.strptime(start_str, '%H:%M').time()
            end_time = datetime.strptime(end_str, '%H:%M').time()
            
            # Check for conflicts with existing bookings
            conflicting = StudioBooking.objects.filter(
                date=date,
                time_slot=slot,
                status__in=['pending', 'confirmed', 'completed']
            )
            
            if self.instance.pk:
                conflicting = conflicting.exclude(pk=self.instance.pk)
            
            if conflicting.exists():
                booking = conflicting.first()
                raise ValidationError(
                    f'该时间段已被 {booking.user.profile.real_name} 预约'
                )
        
        return cleaned_data
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        slot = self.cleaned_data['time_slot']
        
        # Parse time slot and set start_time and end_time
        start_str, end_str = slot.split('-')
        booking.start_time = datetime.strptime(start_str, '%H:%M').time()
        booking.end_time = datetime.strptime(end_str, '%H:%M').time()
        booking.time_slot = slot
        
        if commit:
            booking.save()
        return booking
