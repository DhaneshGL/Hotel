import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Chat, User
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        sender_id = text_data_json['sender_id']
        chat_id = text_data_json['chat_id']

        sender = await sync_to_async(User.objects.get)(id=sender_id)
        chat = await sync_to_async(Chat.objects.get)(id=chat_id)

        message = await sync_to_async(Message.objects.create)(
            chat=chat,
            sender=sender,
            content=message_content
        )

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender_username': sender.username,
                'created_at': str(message.created_at)
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_username = event['sender_username']
        created_at = event['created_at']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender_username': sender_username,
            'created_at': created_at
        }))