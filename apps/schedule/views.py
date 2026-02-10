from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime, date, timedelta
from apps.permissions.decorators import module_permission_required
from .models import Group, DailySchedule, Program, Song
from .forms import GroupForm, DailyScheduleForm, ProgramForm, SongForm


@login_required
def calendar_view(request):
    """Display the calendar view with FullCalendar"""
    return render(request, 'schedule/calendar.html')


@login_required
def calendar_events_api(request):
    """JSON API for FullCalendar events"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    events = []
    
    if start and end:
        start_date = datetime.strptime(start[:10], '%Y-%m-%d').date()
        end_date = datetime.strptime(end[:10], '%Y-%m-%d').date()
        
        schedules = DailySchedule.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).prefetch_related('anchors', 'programs', 'songs')
        
        for schedule in schedules:
            anchor_names = ', '.join([
                a.profile.real_name if hasattr(a, 'profile') else a.username 
                for a in schedule.anchors.all()
            ])
            
            events.append({
                'title': f'已排班 - {anchor_names}' if anchor_names else '已排班',
                'start': schedule.date.isoformat(),
                'url': f'/broadcast/calendar/{schedule.date}/',
                'classNames': ['cursor-pointer'],
            })
    
    return JsonResponse(events, safe=False)


@login_required
def day_detail_view(request, date_str):
    """Show/edit single day schedule (modal content)"""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, '日期格式错误')
        return redirect('schedule:calendar')
    
    schedule, created = DailySchedule.objects.get_or_create(
        date=target_date,
        defaults={'created_by': request.user}
    )
    
    # Check if there are bookings for this date
    bookings = []
    try:
        from apps.booking.models import Booking
        bookings = Booking.objects.filter(
            date=target_date,
            status='approved'
        ).select_related('user')
    except:
        pass
    
    context = {
        'schedule': schedule,
        'date': target_date,
        'weekday': target_date.isoweekday(),
        'bookings': bookings,
    }
    
    return render(request, 'schedule/day_detail.html', context)


@module_permission_required('schedule')
@require_POST
def add_program_view(request, date_str):
    """Add program to a day"""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, '日期格式错误')
        return redirect('schedule:calendar')
    
    schedule, created = DailySchedule.objects.get_or_create(
        date=target_date,
        defaults={'created_by': request.user}
    )
    
    form = ProgramForm(request.POST)
    if form.is_valid():
        program = form.save(commit=False)
        program.schedule = schedule
        program.save()
        messages.success(request, '节目添加成功')
    else:
        messages.error(request, '节目添加失败')
    
    return redirect('schedule:day_detail', date_str=date_str)


@module_permission_required('schedule')
@require_POST
def delete_program_view(request, pk):
    """Delete a program"""
    program = get_object_or_404(Program, pk=pk)
    date_str = program.schedule.date.strftime('%Y-%m-%d')
    program.delete()
    messages.success(request, '节目删除成功')
    return redirect('schedule:day_detail', date_str=date_str)


@module_permission_required('schedule')
@require_POST
def add_song_view(request, date_str):
    """Add song to a day"""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, '日期格式错误')
        return redirect('schedule:calendar')
    
    schedule, created = DailySchedule.objects.get_or_create(
        date=target_date,
        defaults={'created_by': request.user}
    )
    
    form = SongForm(request.POST)
    if form.is_valid():
        song = form.save(commit=False)
        song.schedule = schedule
        song.save()
        messages.success(request, '歌曲添加成功')
    else:
        messages.error(request, '歌曲添加失败')
    
    return redirect('schedule:day_detail', date_str=date_str)


@module_permission_required('schedule')
@require_POST
def delete_song_view(request, pk):
    """Delete a song"""
    song = get_object_or_404(Song, pk=pk)
    date_str = song.schedule.date.strftime('%Y-%m-%d')
    song.delete()
    messages.success(request, '歌曲删除成功')
    return redirect('schedule:day_detail', date_str=date_str)


@module_permission_required('schedule')
@require_POST
def fill_from_group_view(request, date_str):
    """Auto-fill anchors from group based on weekday"""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, '日期格式错误')
        return redirect('schedule:calendar')
    
    schedule, created = DailySchedule.objects.get_or_create(
        date=target_date,
        defaults={'created_by': request.user}
    )
    
    weekday = target_date.isoweekday()
    
    try:
        group = Group.objects.get(weekday=weekday)
        # Clear existing anchors and add group members
        schedule.anchors.clear()
        
        # Add leader first if exists
        if group.leader:
            schedule.anchors.add(group.leader)
        
        # Add all members
        for member in group.members.all():
            schedule.anchors.add(member)
        
        # Count total anchors added
        total_count = schedule.anchors.count()
        messages.success(request, f'已从 {group.name} 填充 {total_count} 位播音员')
    except Group.DoesNotExist:
        messages.warning(request, f'该日期（{target_date.strftime("%A")}）没有对应的分组')
    
    return redirect('schedule:day_detail', date_str=date_str)


@module_permission_required('schedule')
@require_POST
def copy_previous_day_view(request, date_str):
    """Copy schedule from previous day"""
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, '日期格式错误')
        return redirect('schedule:calendar')
    
    previous_date = target_date - timedelta(days=1)
    
    try:
        previous_schedule = DailySchedule.objects.get(date=previous_date)
        
        # Get or create current day's schedule
        schedule, created = DailySchedule.objects.get_or_create(
            date=target_date,
            defaults={'created_by': request.user}
        )
        
        # Copy anchors
        schedule.anchors.clear()
        for anchor in previous_schedule.anchors.all():
            schedule.anchors.add(anchor)
        
        # Copy programs
        schedule.programs.all().delete()
        for program in previous_schedule.programs.all():
            Program.objects.create(
                schedule=schedule,
                name=program.name,
                time_slot=program.time_slot,
                order=program.order
            )
        
        # Copy songs
        schedule.songs.all().delete()
        for song in previous_schedule.songs.all():
            Song.objects.create(
                schedule=schedule,
                title=song.title,
                artist=song.artist,
                order=song.order
            )
        
        messages.success(request, f'已从 {previous_date.strftime("%Y-%m-%d")} 复制排班数据')
    except DailySchedule.DoesNotExist:
        messages.warning(request, f'前一天 ({previous_date.strftime("%Y-%m-%d")}) 没有排班数据')
    
    return redirect('schedule:day_detail', date_str=date_str)


@module_permission_required('schedule')
@require_POST
def create_week_schedule_view(request):
    """Batch create weekly schedules from groups"""
    start_date_str = request.POST.get('start_date')
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        messages.error(request, '请提供有效的开始日期')
        return redirect('schedule:calendar')
    
    # Create schedules for the next 7 days
    created_count = 0
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        weekday = current_date.isoweekday()
        
        # Get or create schedule for this day
        schedule, created = DailySchedule.objects.get_or_create(
            date=current_date,
            defaults={'created_by': request.user}
        )
        
        # Try to fill from group
        try:
            group = Group.objects.get(weekday=weekday)
            schedule.anchors.clear()
            
            if group.leader:
                schedule.anchors.add(group.leader)
            
            for member in group.members.all():
                schedule.anchors.add(member)
            
            if created:
                created_count += 1
        except Group.DoesNotExist:
            pass
    
    messages.success(request, f'成功创建一周排班，共 {created_count} 天新排班')
    return redirect('schedule:calendar')


@login_required
def groups_list_view(request):
    """Show all 6 groups"""
    groups = Group.objects.all().prefetch_related('leader', 'members')
    return render(request, 'schedule/groups.html', {'groups': groups})


@module_permission_required('groups')
def group_edit_view(request, pk):
    """Edit group (permission required)"""
    group = get_object_or_404(Group, pk=pk)
    
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, f'{group.name}更新成功')
            return redirect('schedule:groups_list')
    else:
        form = GroupForm(instance=group)
    
    return render(request, 'schedule/group_edit.html', {
        'form': form,
        'group': group,
    })
