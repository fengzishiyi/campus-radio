from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list_view, name='list'),
    path('create/', views.news_create_view, name='create'),
    path('stats/', views.news_stats_view, name='stats'),
    path('<int:pk>/', views.news_detail_view, name='detail'),
    path('<int:pk>/edit/', views.news_edit_view, name='edit'),
    path('<int:pk>/delete/', views.news_delete_view, name='delete'),
]
