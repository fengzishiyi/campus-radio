from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from apps.permissions.decorators import module_permission_required
from .models import StudioBooking
from .forms import StudioBookingForm


@login_required
def booking_calendar_view(request):
    """日历视图显示所有预约"""
    return render(request, 'booking/calendar.html')


@login_required
def booking_events_api(request):
    """FullCalendar API - 返回预约事件JSON"""
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    # 查询指定日期范围内的预约
    bookings = StudioBooking.objects.filter(
        date__gte=start,
        date__lte=end
    ).exclude(status='cancelled')
    
    # 按日期统计预约数量
    booking_counts = {}
    for booking in bookings:
        date_str = booking.date.isoformat()
        if date_str not in booking_counts:
            booking_counts[date_str] = 0
        booking_counts[date_str] += 1
    
    # 生成FullCalendar事件
    events = []
    for date_str, count in booking_counts.items():
        events.append({
            'title': f'{count} 个预约',
            'start': date_str,
            'url': f'/booking/{date_str}/',
            'display': 'background',
            'backgroundColor': '#3b82f6' if count < 5 else '#ef4444'
        })
    
    return JsonResponse(events, safe=False)


@login_required
def day_bookings_view(request, date):
    """显示某天的预约时间线（8:00-22:00）"""
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    
    # 查询当天所有预约
    bookings = StudioBooking.objects.filter(date=date_obj).exclude(status='cancelled')
    
    # 生成时间块数据
    bookings_data = []
    for booking in bookings:
        # 计算开始和结束时间相对于8:00的小时数
        start_hour = booking.start_time.hour + booking.start_time.minute / 60
        end_hour = booking.end_time.hour + booking.end_time.minute / 60
        
        # 计算位置和宽度（相对于8:00-22:00的14小时）
        start_offset = ((start_hour - 8) / 14) * 100
        width = ((end_hour - start_hour) / 14) * 100
        
        # 根据状态设置颜色
        color_map = {
            'pending': 'bg-yellow-400',
            'confirmed': 'bg-blue-500',
            'completed': 'bg-green-500',
            'cancelled': 'bg-gray-400'
        }
        
        bookings_data.append({
            'booking': booking,
            'start_offset': start_offset,
            'width': width,
            'color': color_map.get(booking.status, 'bg-gray-400')
        })
    
    context = {
        'date': date_obj,
        'bookings_data': bookings_data,
        'hours': range(8, 23)  # 8:00 到 22:00
    }
    
    return render(request, 'booking/day_timeline.html', context)


@module_permission_required('booking')
def booking_create_view(request):
    """创建预约"""
    if request.method == 'POST':
        form = StudioBookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.user = request.user
                booking.status = 'confirmed'
                booking.save()
                messages.success(request, '预约创建成功！')
                return redirect('booking:my_bookings')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, '表单填写有误，请检查后重试。')
    else:
        # 预填充默认值
        initial = {}
        if 'date' in request.GET:
            initial['date'] = request.GET['date']
        form = StudioBookingForm(initial=initial)
    
    return render(request, 'booking/form.html', {'form': form})


@login_required
def my_bookings_view(request):
    """显示当前用户的预约"""
    bookings = StudioBooking.objects.filter(user=request.user).order_by('-date', '-start_time')
    
    # Calculate statistics
    confirmed_count = bookings.filter(status='confirmed').count()
    pending_count = bookings.filter(status='pending').count()
    completed_count = bookings.filter(status='completed').count()
    
    context = {
        'bookings': bookings,
        'confirmed_count': confirmed_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
    }
    
    return render(request, 'booking/my_bookings.html', context)


@login_required
def booking_cancel_view(request, pk):
    """取消预约"""
    booking = get_object_or_404(StudioBooking, pk=pk)
    
    # 检查权限：只有预约者本人或管理员可以取消
    is_admin = hasattr(request.user, 'profile') and request.user.profile.is_admin()
    if booking.user != request.user and not is_admin:
        messages.error(request, '您没有权限取消此预约。')
        return redirect('booking:my_bookings')
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, '预约已取消。')
        return redirect('booking:my_bookings')
    
    return render(request, 'booking/cancel_confirm.html', {'booking': booking})
