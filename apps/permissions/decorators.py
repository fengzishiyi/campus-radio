from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ModulePermission


def module_permission_required(module_name):
    """Check if user has permission to edit a module"""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                module_perm = ModulePermission.objects.get(module_name=module_name, is_active=True)
                if not module_perm.can_edit(request.user):
                    messages.error(request, f'您没有权限访问该模块')
                    return redirect('/')
            except ModulePermission.DoesNotExist:
                messages.error(request, f'模块权限配置不存在')
                return redirect('/')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    """Check if user is admin"""
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
            messages.error(request, '只有管理员可以访问此页面')
            return redirect('/')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
