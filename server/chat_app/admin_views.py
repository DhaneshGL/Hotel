from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from .models import User, Chat, Message
from .serializers import UserSerializer, ChatSerializer, MessageSerializer
from datetime import datetime, timedelta
import jwt
from django.conf import settings

@api_view(['POST'])
def admin_login(request):
    secret_key = request.data.get('secretKey')
    if secret_key == 'admin_secret_key':  
        token = jwt.encode({'secretKey': secret_key}, settings.SECRET_KEY, algorithm='HS256')
        response = Response({'message': 'Authenticated Successfully, Welcome BOSS'})
        response.set_cookie('chattu-admin-token', token, httponly=True, samesite='Lax', max_age=15 * 60)
        return response
    return Response({'message': 'Invalid Admin Key'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def admin_logout(request):
    response = Response({'message': 'Logged Out Successfully'})
    response.delete_cookie('chattu-admin-token')
    return response

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_admin_data(request):
    return Response({'admin': True})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_users(request):
    users = User.objects.all()
    transformed_users = []
    for user in users:
        groups_count = Chat.objects.filter(group_chat=True, members=user).count()
        friends_count = Chat.objects.filter(group_chat=False, members=user).count()
        transformed_users.append({
            'id': user.id,
            'name': user.username,
            'email': user.email,
            'avatar': user.avatar_url,
            'groups': groups_count,
            'friends': friends_count,
        })
    return Response({'users': transformed_users})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_chats(request):
    chats = Chat.objects.all().prefetch_related('members').select_related('creator')
    transformed_chats = []
    for chat in chats:
        total_messages = Message.objects.filter(chat=chat).count()
        transformed_chats.append({
            'id': chat.id,
            'groupChat': chat.group_chat,
            'name': chat.name,
            'avatar': [member.avatar_url for member in chat.members.all()[:3]],
            'members': [{'id': member.id, 'name': member.username, 'avatar': member.avatar_url} for member in chat.members.all()],
            'creator': {'name': chat.creator.username if chat.creator else 'None', 'avatar': chat.creator.avatar_url if chat.creator else ''},
            'totalMembers': chat.members.count(),
            'totalMessages': total_messages,
        })
    return Response({'chats': transformed_chats})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_messages(request):
    messages = Message.objects.all().select_related('sender', 'chat')
    transformed_messages = []
    for message in messages:
        transformed_messages.append({
            'id': message.id,
            'attachments': message.attachments,
            'content': message.content,
            'createdAt': message.created_at,
            'chat': message.chat.id,
            'groupChat': message.chat.group_chat,
            'sender': {
                'id': message.sender.id,
                'name': message.sender.username,
                'avatar': message.sender.avatar_url,
            },
        })
    return Response({'messages': transformed_messages})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_dashboard_stats(request):
    groups_count = Chat.objects.filter(group_chat=True).count()
    users_count = User.objects.count()
    messages_count = Message.objects.count()
    total_chats_count = Chat.objects.count()

    today = datetime.now()
    last_7_days = today - timedelta(days=7)

    last_7_days_messages = Message.objects.filter(created_at__gte=last_7_days, created_at__lte=today).order_by('created_at')
    last_7_days_chats = Chat.objects.filter(created_at__gte=last_7_days, created_at__lte=today).order_by('created_at')
    last_7_days_users = User.objects.filter(date_joined__gte=last_7_days, date_joined__lte=today).order_by('date_joined')

    messages_chart = [0] * 7
    chats_chart = [0] * 7
    users_chart = [0] * 7

    for message in last_7_days_messages:
        index = (today - message.created_at).days
        if 0 <= index < 7:
            messages_chart[6 - index] += 1

    for chat in last_7_days_chats:
        index = (today - chat.created_at).days
        if 0 <= index < 7:
            chats_chart[6 - index] += 1

    for user in last_7_days_users:
        index = (today - user.date_joined).days
        if 0 <= index < 7:
            users_chart[6 - index] += 1

    stats = {
        'groupsCount': groups_count,
        'usersCount': users_count,
        'messagesCount': messages_count,
        'totalChatsCount': total_chats_count,
        'messagesChart': messages_chart,
        'chatsChart': chats_chart,
        'usersChart': users_chart,
    }

    return Response({'stats': stats})