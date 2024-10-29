from django.urls import path
from . import admin_views

urlpatterns = [
    path('admin-login/', admin_views.admin_login, name='admin_login'),
    path('admin-logout/', admin_views.admin_logout, name='admin_logout'),
    path('admin-data/', admin_views.get_admin_data, name='get_admin_data'),
    path('users/', admin_views.all_users, name='all_users'),
    path('chats/', admin_views.all_chats, name='all_chats'),
    path('messages/', admin_views.all_messages, name='all_messages'),
    path('dashboard-stats/', admin_views.get_dashboard_stats, name='get_dashboard_stats'),
]