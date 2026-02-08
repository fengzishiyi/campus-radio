from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_calendar_view, name='calendar'),
    path('api/events/', views.booking_events_api, name='events_api'),
    path('create/', views.booking_create_view, name='create'),
    path('my/', views.my_bookings_view, name='my_bookings'),
    path('<int:pk>/cancel/', views.booking_cancel_view, name='cancel'),
    path('<str:date>/', views.day_bookings_view, name='day_timeline'),
]
