import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # گرفتن group_name از URL
        self.room_group_name = self.scope['url_route']['kwargs']['group_name']

        # احراز هویت با توکن JWT
        token = self.scope['query_string'].decode().split('token=')[-1]
        user = await self.authenticate_user(token)
        if not user:
            await self.close()
            return

        self.user = user

        # اضافه کردن به گروه
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # ارسال پیام خوش‌آمدگویی
        current_time = timezone.now().strftime("%H:%M:%S")
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': f'سلام {self.user.username} الان ساعت {current_time} است'
        }))

    @database_sync_to_async
    def authenticate_user(self, token):
        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            return user
        except (InvalidToken, TokenError):
            return None

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def chat_message(self, event):
        # ارسال پیام به کلاینت
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message']
        }))