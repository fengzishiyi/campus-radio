"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        from apps.announcements.models import Announcement
        from apps.booking.models import StudioBooking
        from apps.schedule.models import DailySchedule
        from django.db.models import Q
        from django.utils import timezone
        
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_authenticated:
            # 最新公告（6条）
            context['recent_announcements'] = Announcement.objects.filter(
                Q(target_department='all') | Q(target_department=self.request.user.profile.department)
            ).filter(
                Q(expire_time__isnull=True) | Q(expire_time__gt=timezone.now())
            )[:6]
            
            # 今日数据
            today = timezone.now().date()
            
            # 今日录音室预约
            today_bookings = StudioBooking.objects.filter(
                date=today
            ).exclude(status='cancelled').select_related('user', 'user__profile').order_by('start_time')
            
            # 计算时间轴数据（基于8:00-22:00，14小时范围）
            bookings_with_offset = []
            for booking in today_bookings:
                start_hour = booking.start_time.hour + booking.start_time.minute / 60
                end_hour = booking.end_time.hour + booking.end_time.minute / 60
                
                start_offset = ((start_hour - 8) / 14) * 100
                width = ((end_hour - start_hour) / 14) * 100
                
                bookings_with_offset.append({
                    'user': booking.user,
                    'start_time': booking.start_time,
                    'end_time': booking.end_time,
                    'purpose': booking.purpose,
                    'status': booking.status,
                    'start_offset': max(0, min(100, start_offset)),
                    'width': max(0, min(100 - start_offset, width))
                })
            
            context['today_bookings'] = bookings_with_offset
            context['today_bookings_count'] = today_bookings.count()
            context['timeline_hours'] = range(8, 23)
            
            # 今日歌单和节目
            try:
                today_schedule = DailySchedule.objects.prefetch_related('songs', 'programs').get(date=today)
                context['today_songs'] = today_schedule.songs.all().order_by('order')[:15]
                context['today_programs'] = today_schedule.programs.all().order_by('order')
            except DailySchedule.DoesNotExist:
                context['today_songs'] = []
                context['today_programs'] = []
        
        return context

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_required(HomeView.as_view()), name='home'),
    path('accounts/', include('apps.accounts.urls')),
    path('admin/permissions/', include('apps.permissions.urls')),
    path('announcements/', include('apps.announcements.urls')),
    path('broadcast/news/', include('apps.news.urls')),
    path('broadcast/', include('apps.schedule.urls')),
    path('booking/', include('apps.booking.urls')),
    path('himalaya/', include('apps.himalaya.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
