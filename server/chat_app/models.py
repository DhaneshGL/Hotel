from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.CharField(max_length=200, default='Bio')
    avatar_public_id = models.CharField(max_length=255)
    avatar_url = models.URLField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Chat(models.Model):
    name = models.CharField(max_length=255)
    group_chat = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_chats')
    members = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        if self.group_chat:
            return self.name
        return ", ".join([member.username for member in self.members.all()])

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField(blank=True, null=True)
    attachments = models.JSONField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.chat.name}"

class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, default='pending')  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.sender.username} to {self.receiver.username}"

class Code(models.Model):
    code = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Code for {self.email}"
