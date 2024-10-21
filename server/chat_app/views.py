from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import User, Chat, Message, Request
from .serializers import UserSerializer, ChatSerializer, MessageSerializer, RequestSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    logout(request)
    return Response({'message': 'Logged out successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_user(request):
    query = request.query_params.get('query', '')
    users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query)).exclude(id=request.user.id)
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_request(request):
    receiver_id = request.data.get('receiver_id')
    receiver = get_object_or_404(User, id=receiver_id)
    if Request.objects.filter(sender=request.user, receiver=receiver).exists():
        return Response({'message': 'Request already sent'}, status=status.HTTP_400_BAD_REQUEST)
    req = Request.objects.create(sender=request.user, receiver=receiver)
    serializer = RequestSerializer(req)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request):
    request_id = request.data.get('request_id')
    req = get_object_or_404(Request, id=request_id, receiver=request.user)
    req.status = 'accepted'
    req.save()
    chat = Chat.objects.create(group_chat=False, creator=request.user)
    chat.members.add(request.user, req.sender)
    serializer = ChatSerializer(chat)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_notifications(request):
    notifications = Request.objects.filter(receiver=request.user, status='pending')
    serializer = RequestSerializer(notifications, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_chats(request):
    chats = request.user.chats.all()
    serializer = ChatSerializer(chats, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chat_details(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, members=request.user)
    serializer = ChatSerializer(chat)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_messages(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, members=request.user)
    messages = chat.messages.all().order_by('created_at')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_group_chat(request):
    name = request.data.get('name')
    members_ids = request.data.get('members', [])
    members = User.objects.filter(id__in=members_ids)
    if not name or not members:
        return Response({'message': 'Name and members are required'}, status=status.HTTP_400_BAD_REQUEST)
    chat = Chat.objects.create(name=name, group_chat=True, creator=request.user)
    chat.members.add(request.user, *members)
    serializer = ChatSerializer(chat)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_members(request):
    chat_id = request.data.get('chat_id')
    members_ids = request.data.get('members', [])
    chat = get_object_or_404(Chat, id=chat_id, creator=request.user, group_chat=True)
    new_members = User.objects.filter(id__in=members_ids)
    chat.members.add(*new_members)
    serializer = ChatSerializer(chat)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_member(request):
    chat_id = request.data.get('chat_id')
    member_id = request.data.get('member_id')
    chat = get_object_or_404(Chat, id=chat_id, creator=request.user, group_chat=True)
    member_to_remove = get_object_or_404(User, id=member_id)
    chat.members.remove(member_to_remove)
    serializer = ChatSerializer(chat)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_group(request):
    chat_id = request.data.get('chat_id')
    chat = get_object_or_404(Chat, id=chat_id, members=request.user, group_chat=True)
    chat.members.remove(request.user)
    if chat.members.count() == 0:
        chat.delete()
    elif chat.creator == request.user:
        chat.creator = chat.members.first()
        chat.save()
    return Response({'message': 'Left group successfully'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, creator=request.user)
    chat.delete()
    return Response({'message': 'Chat deleted successfully'})
