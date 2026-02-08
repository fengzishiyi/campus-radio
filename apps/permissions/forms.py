from django import forms
from .models import ModulePermission


class ModulePermissionForm(forms.ModelForm):
    """Form to edit allowed_roles for a module"""
    
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('anchor', '播音员'),
        ('himalaya', '喜马拉雅人员'),
    ]
    
    roles = forms.MultipleChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='允许的角色'
    )
    
    class Meta:
        model = ModulePermission
        fields = ['module_label', 'is_active']
        widgets = {
            'module_label': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded border-gray-300 text-blue-600 focus:ring-blue-500'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['roles'].initial = self.instance.allowed_roles
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.allowed_roles = self.cleaned_data.get('roles', [])
        if commit:
            instance.save()
        return instance
