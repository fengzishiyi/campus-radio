from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    # Calendar views
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/api/events/', views.calendar_events_api, name='calendar_events_api'),
    path('calendar/<str:date_str>/', views.day_detail_view, name='day_detail'),
    
    # Program management
    path('calendar/<str:date_str>/add-program/', views.add_program_view, name='add_program'),
    path('programs/<int:pk>/delete/', views.delete_program_view, name='delete_program'),
    
    # Song management
    path('calendar/<str:date_str>/add-song/', views.add_song_view, name='add_song'),
    path('songs/<int:pk>/delete/', views.delete_song_view, name='delete_song'),
    
    # Batch operations
    path('calendar/<str:date_str>/fill-from-group/', views.fill_from_group_view, name='fill_from_group'),
    path('calendar/<str:date_str>/copy-previous/', views.copy_previous_day_view, name='copy_previous_day'),
    path('calendar/create-week/', views.create_week_schedule_view, name='create_week'),
    
    # Groups management
    path('groups/', views.groups_list_view, name='groups_list'),
    path('groups/<int:pk>/edit/', views.group_edit_view, name='group_edit'),
]
