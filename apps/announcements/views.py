from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from apps.permissions.decorators import module_permission_required
from .models import Announcement
from .forms import AnnouncementForm


@login_required
def announcement_list_view(request):
    """List all announcements with filtering"""
    # Get filter parameters
    filter_type = request.GET.get('type', '')
    filter_department = request.GET.get('department', '')
    
    # Base queryset - show announcements for user's department and 'all'
    announcements = Announcement.objects.filter(
        Q(target_department='all') | Q(target_department=request.user.profile.department)
    )
    
    # Filter out expired announcements
    announcements = announcements.filter(
        Q(expire_time__isnull=True) | Q(expire_time__gt=timezone.now())
    )
    
    # Apply type filter
    if filter_type:
        announcements = announcements.filter(type=filter_type)
    
    # Apply department filter
    if filter_department:
        announcements = announcements.filter(target_department=filter_department)
    
    # Ordering is already set in model Meta (pinned first, then by publish_time)
    
    context = {
        'announcements': announcements,
        'filter_type': filter_type,
        'filter_department': filter_department,
        'type_choices': Announcement.TYPE_CHOICES,
        'department_choices': Announcement.DEPARTMENT_CHOICES,
    }
    return render(request, 'announcements/list.html', context)


@login_required
def announcement_detail_view(request, pk):
    """View announcement detail and mark as read"""
    announcement = get_object_or_404(Announcement, pk=pk)
    
    # Check if user should see this announcement
    if announcement.target_department not in ['all', request.user.profile.department]:
        messages.error(request, '您没有权限查看此公告')
        return redirect('announcements:list')
    
    # Check if expired
    if announcement.is_expired():
        messages.warning(request, '此公告已过期')
    
    # Mark as read
    if request.user not in announcement.read_by.all():
        announcement.read_by.add(request.user)
    
    context = {
        'announcement': announcement,
        'read_count': announcement.read_by.count(),
    }
    return render(request, 'announcements/detail.html', context)


@module_permission_required('announcements')
def announcement_create_view(request):
    """Create a new announcement"""
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.publisher = request.user
            announcement.save()
            messages.success(request, '公告发布成功！')
            return redirect('announcements:detail', pk=announcement.pk)
    else:
        form = AnnouncementForm()
    
    context = {
        'form': form,
        'title': '发布公告',
        'submit_text': '发布',
    }
    return render(request, 'announcements/form.html', context)


@module_permission_required('announcements')
def announcement_edit_view(request, pk):
    """Edit an existing announcement"""
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, '公告更新成功！')
            return redirect('announcements:detail', pk=announcement.pk)
    else:
        form = AnnouncementForm(instance=announcement)
    
    context = {
        'form': form,
        'title': '编辑公告',
        'submit_text': '保存',
        'announcement': announcement,
    }
    return render(request, 'announcements/form.html', context)


@module_permission_required('announcements')
def announcement_delete_view(request, pk):
    """Delete an announcement"""
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, '公告已删除')
        return redirect('announcements:list')
    
    context = {
        'announcement': announcement,
    }
    return render(request, 'announcements/delete_confirm.html', context)
