from django.urls import path
from . import views

app_name = 'himalaya'

urlpatterns = [
    # Album URLs
    path('', views.album_list_view, name='album_list'),
    path('album/create/', views.album_create_view, name='album_create'),
    path('album/<int:pk>/', views.album_detail_view, name='album_detail'),
    path('album/<int:pk>/edit/', views.album_edit_view, name='album_edit'),
    path('album/<int:pk>/delete/', views.album_delete_view, name='album_delete'),
    
    # Track URLs
    path('album/<int:album_pk>/add-track/', views.track_create_view, name='track_create'),
    path('track/<int:pk>/edit/', views.track_edit_view, name='track_edit'),
    path('track/<int:pk>/delete/', views.track_delete_view, name='track_delete'),
    path('play/<int:pk>/', views.track_play_view, name='track_play'),
    
    # Script URLs
    path('track/<int:pk>/script/', views.script_view, name='script_view'),
    path('track/<int:pk>/script/edit/', views.script_edit_view, name='script_edit'),
]
