from django.urls import path
from . import views

app_name = 'permissions'

urlpatterns = [
    path('config/', views.permissions_config_view, name='config'),
]
