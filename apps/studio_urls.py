"""
Studio URLs - Merged from schedule and booking modules
录音室URL配置 - 合并排班和预约功能
"""
from django.urls import path
from apps.schedule import views as schedule_views
from apps.booking import views as booking_views

app_name = 'studio'

urlpatterns = [
    # Main Calendar View - 日历主页
    path('', schedule_views.calendar_view, name='calendar'),
    path('api/events/', schedule_views.calendar_events_api, name='calendar_events_api'),
    
    # Day Detail View - 日详情页 (merged schedule and booking)
    path('<str:date_str>/', schedule_views.studio_day_detail_view, name='day_detail'),
    
    # Program management - 节目管理
    path('<str:date_str>/add-program/', schedule_views.add_program_view, name='add_program'),
    path('programs/<int:pk>/delete/', schedule_views.delete_program_view, name='delete_program'),
    
    # Song management - 歌曲管理
    path('<str:date_str>/add-song/', schedule_views.add_song_view, name='add_song'),
    path('<str:date_str>/upload-song/', schedule_views.upload_song_view, name='upload_song'),
    path('songs/<int:pk>/delete/', schedule_views.delete_song_view, name='delete_song'),
    
    # Booking management - 预约管理
    path('<str:date_str>/add-booking/', booking_views.booking_create_view, name='add_booking'),
    path('bookings/<int:pk>/cancel/', booking_views.booking_cancel_view, name='cancel_booking'),
    path('my-bookings/', booking_views.my_bookings_view, name='my_bookings'),
    
    # Live broadcast toggle - 直播标记
    path('<str:date_str>/toggle-live/', schedule_views.toggle_live_view, name='toggle_live'),
    
    # Today's playlist API - 今日歌单API (for mini player)
    path('api/today-playlist/', schedule_views.today_playlist_api, name='today_playlist_api'),
    
    # Groups management (keeping for reference)
    path('groups/', schedule_views.groups_list_view, name='groups_list'),
    path('groups/<int:pk>/edit/', schedule_views.group_edit_view, name='group_edit'),
]
