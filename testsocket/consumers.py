import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test_group'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        self.send({'type': 'chat_connected', 'message': 'your connected'})


    def recive(self,text_data):
        messageJson = json.loads(text_data)
        message = messageJson['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message

            }
        )

    def chat_message(self,event):
        message = event['message']
        self.send({'type': 'chat_message', 'message': message})