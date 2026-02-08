from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from .forms import RegistrationForm, UserProfileForm, InviteCodeGenerationForm
from .models import UserProfile, InviteCode
from django.contrib.auth.models import User


def register_view(request):
    """用户注册视图（需要邀请码）"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 创建用户
                    user = form.save()
                    
                    # 创建用户资料
                    UserProfile.objects.create(
                        user=user,
                        real_name=form.cleaned_data['real_name'],
                        student_id=form.cleaned_data['student_id'],
                        phone=form.cleaned_data.get('phone', ''),
                        wechat=form.cleaned_data.get('wechat', ''),
                        department=form.cleaned_data['department'],
                        role=form.cleaned_data['role']
                    )
                    
                    # 标记邀请码为已使用
                    invite_code = form.invite_code_obj
                    invite_code.is_used = True
                    invite_code.used_by = user
                    invite_code.used_at = timezone.now()
                    invite_code.save()
                    
                    # 自动登录
                    login(request, user)
                    messages.success(request, f'欢迎加入，{form.cleaned_data["real_name"]}！')
                    return redirect('accounts:profile')
            except Exception as e:
                messages.error(request, f'注册失败：{str(e)}')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """用户登录视图"""
    if request.user.is_authenticated:
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'欢迎回来，{user.profile.real_name}！')
            next_url = request.GET.get('next', 'accounts:profile')
            return redirect(next_url)
        else:
            messages.error(request, '用户名或密码错误')
    
    return render(request, 'accounts/login.html')


@login_required
def logout_view(request):
    """用户登出视图"""
    logout(request)
    messages.success(request, '您已成功登出')
    return redirect('accounts:login')


@login_required
def profile_edit_view(request):
    """个人资料编辑视图"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '个人资料更新成功！')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {
        'form': form,
        'profile': profile
    })


@login_required
def members_list_view(request):
    """成员列表视图（带搜索和筛选）"""
    members = UserProfile.objects.select_related('user').all()
    
    # 搜索
    search_query = request.GET.get('search', '')
    if search_query:
        members = members.filter(
            Q(real_name__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(user__username__icontains=search_query)
        )
    
    # 部门筛选
    department_filter = request.GET.get('department', '')
    if department_filter:
        members = members.filter(department=department_filter)
    
    # 角色筛选
    role_filter = request.GET.get('role', '')
    if role_filter:
        members = members.filter(role=role_filter)
    
    return render(request, 'accounts/members.html', {
        'members': members,
        'search_query': search_query,
        'department_filter': department_filter,
        'role_filter': role_filter,
        'department_choices': UserProfile.DEPARTMENT_CHOICES,
        'role_choices': UserProfile.ROLE_CHOICES
    })


@login_required
def invite_codes_view(request):
    """邀请码管理视图（仅管理员）"""
    if not request.user.profile.is_admin():
        messages.error(request, '您没有权限访问此页面')
        return redirect('accounts:profile')
    
    codes = InviteCode.objects.select_related('created_by', 'used_by').all()
    used_count = codes.filter(is_used=True).count()
    unused_count = codes.filter(is_used=False).count()
    
    return render(request, 'accounts/invite_codes.html', {
        'codes': codes,
        'used_count': used_count,
        'unused_count': unused_count
    })


@login_required
def generate_invite_code(request):
    """生成邀请码（仅管理员）"""
    if not request.user.profile.is_admin():
        messages.error(request, '您没有权限执行此操作')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        form = InviteCodeGenerationForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            codes = form.generate_codes(request.user, count)
            messages.success(request, f'成功生成 {count} 个邀请码！')
            return redirect('accounts:invite_codes')
    
    return redirect('accounts:invite_codes')
