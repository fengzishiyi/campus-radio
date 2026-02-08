from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_edit_view, name='profile'),
    path('members/', views.members_list_view, name='members'),
    path('invite-codes/', views.invite_codes_view, name='invite_codes'),
    path('invite-codes/generate/', views.generate_invite_code, name='generate_invite_code'),
]
