from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import models
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
    """JSON API for FullCalendar events - includes schedules and bookings"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    events = []
    
    if start and end:
        start_date = datetime.strptime(start[:10], '%Y-%m-%d').date()
        end_date = datetime.strptime(end[:10], '%Y-%m-%d').date()
        
        # Add schedule events
        schedules = DailySchedule.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).prefetch_related('anchors', 'programs', 'songs')
        
        for schedule in schedules:
            anchor_names = ', '.join([
                a.profile.real_name if hasattr(a, 'profile') else a.username 
                for a in schedule.anchors.all()
            ])
            
            title = f'已排班'
            if anchor_names:
                title += f' - {anchor_names}'
            if schedule.is_live:
                title += ' 📡'
            
            events.append({
                'title': title,
                'start': schedule.date.isoformat(),
                'url': f'/studio/{schedule.date}/',
                'classNames': ['cursor-pointer'],
                'color': '#0969da' if not schedule.is_live else '#ff6b6b',
            })
        
        # Add booking events
        from apps.booking.models import StudioBooking
        bookings = StudioBooking.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        ).exclude(status='cancelled').select_related('user', 'user__profile')
        
        for booking in bookings:
            events.append({
                'title': f'预约 - {booking.user.profile.real_name}',
                'start': f'{booking.date}T{booking.start_time}',
                'end': f'{booking.date}T{booking.end_time}',
                'url': f'/studio/{booking.date}/',
                'classNames': ['cursor-pointer'],
                'color': '#2da44e',
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


# ==================== New Studio Views (Merged functionality) ====================

@login_required
def studio_day_detail_view(request, date_str):
    """
    Unified day detail view combining schedule, songs, programs and bookings
    合并的日详情页：显示排班、歌曲、节目和预约
    """
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, '日期格式错误')
        return redirect('studio:calendar')
    
    schedule, created = DailySchedule.objects.get_or_create(
        date=target_date,
        defaults={'created_by': request.user}
    )
    
    # Get bookings for this date
    from apps.booking.models import StudioBooking
    bookings = StudioBooking.objects.filter(
        date=target_date
    ).exclude(status='cancelled').select_related('user', 'user__profile').order_by('start_time')
    
    # Calculate timeline data for bookings (8:00-22:00)
    STUDIO_OPEN_HOUR = 8
    STUDIO_CLOSE_HOUR = 22
    STUDIO_OPERATING_HOURS = STUDIO_CLOSE_HOUR - STUDIO_OPEN_HOUR
    
    bookings_with_offset = []
    for booking in bookings:
        start_hour = booking.start_time.hour + booking.start_time.minute / 60
        end_hour = booking.end_time.hour + booking.end_time.minute / 60
        
        start_offset = ((start_hour - STUDIO_OPEN_HOUR) / STUDIO_OPERATING_HOURS) * 100
        width = ((end_hour - start_hour) / STUDIO_OPERATING_HOURS) * 100
        
        bookings_with_offset.append({
            'id': booking.id,
            'user': booking.user,
            'start_time': booking.start_time,
            'end_time': booking.end_time,
            'purpose': booking.purpose,
            'status': booking.status,
            'start_offset': max(0, min(100, start_offset)),
            'width': max(0, min(100 - start_offset, width))
        })
    
    # Check if live broadcast (16:00-18:00)
    if schedule.is_live:
        # Add live broadcast block
        live_start_hour = 16
        live_end_hour = 18
        live_start_offset = ((live_start_hour - STUDIO_OPEN_HOUR) / STUDIO_OPERATING_HOURS) * 100
        live_width = ((live_end_hour - live_start_hour) / STUDIO_OPERATING_HOURS) * 100
        
        bookings_with_offset.append({
            'id': None,
            'user': None,
            'start_time': None,
            'end_time': None,
            'purpose': '📡 直播中',
            'status': 'live',
            'start_offset': live_start_offset,
            'width': live_width,
            'is_live': True
        })
    
    context = {
        'schedule': schedule,
        'date': target_date,
        'weekday': target_date.isoweekday(),
        'programs': schedule.programs.all().order_by('order'),
        'songs': schedule.songs.all().order_by('order'),
        'bookings': bookings_with_offset,
        'timeline_hours': range(STUDIO_OPEN_HOUR, STUDIO_CLOSE_HOUR + 1),
        'program_form': ProgramForm(),
        'song_form': SongForm(),
    }
    
    return render(request, 'studio/day_detail.html', context)


@module_permission_required('schedule')
@require_POST
def upload_song_view(request, date_str):
    """
    Upload audio file for a song
    上传歌曲音频文件
    """
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': '日期格式错误'}, status=400)
    
    schedule, created = DailySchedule.objects.get_or_create(
        date=target_date,
        defaults={'created_by': request.user}
    )
    
    title = request.POST.get('title')
    artist = request.POST.get('artist', '')
    audio_file = request.FILES.get('audio_file')
    
    if not title:
        return JsonResponse({'error': '歌曲名不能为空'}, status=400)
    
    if not audio_file:
        return JsonResponse({'error': '请上传音频文件'}, status=400)
    
    # Get the max order
    max_order = schedule.songs.aggregate(models.Max('order'))['order__max'] or 0
    
    song = Song.objects.create(
        schedule=schedule,
        title=title,
        artist=artist,
        audio_file=audio_file,
        order=max_order + 1
    )
    
    return JsonResponse({
        'success': True,
        'song': {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'audio_url': song.audio_file.url if song.audio_file else None
        }
    })


@module_permission_required('schedule')
@require_POST
def toggle_live_view(request, date_str):
    """
    Toggle live broadcast status for a day
    切换直播状态
    """
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, '日期格式错误')
        return redirect('studio:calendar')
    
    schedule, created = DailySchedule.objects.get_or_create(
        date=target_date,
        defaults={'created_by': request.user}
    )
    
    schedule.is_live = not schedule.is_live
    schedule.save()
    
    if schedule.is_live:
        messages.success(request, '已开启直播标记 (16:00-18:00)')
    else:
        messages.success(request, '已关闭直播标记')
    
    return redirect('studio:day_detail', date_str=date_str)


@login_required
def today_playlist_api(request):
    """
    API endpoint to get today's playlist for mini player
    获取今日歌单API（用于迷你播放器）
    """
    from django.utils import timezone
    
    today = timezone.now().date()
    
    try:
        schedule = DailySchedule.objects.prefetch_related('songs').get(date=today)
        songs = []
        for song in schedule.songs.all().order_by('order'):
            songs.append({
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'audio_url': song.audio_file.url if song.audio_file else None
            })
        
        return JsonResponse({'songs': songs})
    except DailySchedule.DoesNotExist:
        return JsonResponse({'songs': []})
