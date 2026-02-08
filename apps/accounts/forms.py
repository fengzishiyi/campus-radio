from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, InviteCode
import secrets


class RegistrationForm(UserCreationForm):
    """用户注册表单（带邀请码验证）"""
    
    username = forms.CharField(
        label='用户名',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请输入用户名'
        })
    )
    
    password1 = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请输入密码'
        })
    )
    
    password2 = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请再次输入密码'
        })
    )
    
    invite_code = forms.CharField(
        label='邀请码',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请输入邀请码'
        })
    )
    
    real_name = forms.CharField(
        label='姓名',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请输入真实姓名'
        })
    )
    
    student_id = forms.CharField(
        label='学号',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请输入学号'
        })
    )
    
    phone = forms.CharField(
        label='手机号',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请输入手机号（选填）'
        })
    )
    
    wechat = forms.CharField(
        label='微信号',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请输入微信号（选填）'
        })
    )
    
    department = forms.ChoiceField(
        label='所属部门',
        choices=UserProfile.DEPARTMENT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    role = forms.ChoiceField(
        label='角色',
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def clean_invite_code(self):
        code = self.cleaned_data.get('invite_code')
        try:
            invite = InviteCode.objects.get(code=code)
            if invite.is_used:
                raise forms.ValidationError('该邀请码已被使用')
            self.invite_code_obj = invite
        except InviteCode.DoesNotExist:
            raise forms.ValidationError('无效的邀请码')
        return code
    
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        if UserProfile.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError('该学号已被注册')
        return student_id


class UserProfileForm(forms.ModelForm):
    """用户资料编辑表单"""
    
    real_name = forms.CharField(
        label='姓名',
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    phone = forms.CharField(
        label='手机号',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    wechat = forms.CharField(
        label='微信号',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    bio = forms.CharField(
        label='个人简介',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'rows': 4,
            'placeholder': '介绍一下自己吧...'
        })
    )
    
    avatar = forms.ImageField(
        label='头像',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    class Meta:
        model = UserProfile
        fields = ['real_name', 'phone', 'wechat', 'avatar', 'bio']


class InviteCodeGenerationForm(forms.Form):
    """邀请码生成表单"""
    
    count = forms.IntegerField(
        label='生成数量',
        min_value=1,
        max_value=100,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': '请输入生成数量（1-100）'
        })
    )
    
    def generate_codes(self, user, count):
        """生成指定数量的邀请码"""
        codes = []
        for _ in range(count):
            code = secrets.token_urlsafe(16)
            invite_code = InviteCode.objects.create(
                code=code,
                created_by=user
            )
            codes.append(invite_code)
        return codes
