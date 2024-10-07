from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('profile/', views.get_my_profile, name='get_my_profile'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', views.search_user, name='search_user'),
    path('send-request/', views.send_request, name='send_request'),
    path('accept-request/', views.accept_request, name='accept_request'),
    path('get-notifications/', views.get_all_notifications, name='get_all_notifications'),
    path('my-chats/', views.get_my_chats, name='get_my_chats'),
    path('my-chats/<int:chat_id>/', views.get_chat_details, name='get_chat_details'),
    path('my-chats/<int:chat_id>/messages/', views.get_messages, name='get_messages'),
    path('new-group-chat/', views.new_group_chat, name='new_group_chat'),
    path('add-members/', views.add_members, name='add_members'),
    path('remove-member/', views.remove_member, name='remove_member'),
    path('leave-group/', views.leave_group, name='leave_group'),
    path('delete-chat/<int:chat_id>/', views.delete_chat, name='delete_chat'),
]