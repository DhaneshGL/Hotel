from rest_framework import serializers
from .models import User, Chat, Message, Request

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar_url']

class ChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'group_chat', 'creator', 'members']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    chat = serializers.PrimaryKeyRelatedField(queryset=Chat.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'chat', 'sender', 'content', 'attachments', 'created_at']

class RequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = Request
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']

class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['id', 'code', 'email']