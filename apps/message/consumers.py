import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        # Import the models here to avoid circular import issues
        from .models import Message
        from apps.accounts.models import Account

        if not self.scope['user'].username:
            await self.close()

        # Get the unique username of the user the current user is trying to chat with
        self.receiver_username = self.scope['url_route']['kwargs']['username']
        self.receiver = await sync_to_async(Account.objects.get)(username=self.receiver_username)

        
        # Create a unique room name for the chat between the current user and the receiver
        self.room_name = f"chat_{min(self.scope['user'].username, self.receiver_username)}_{max(self.scope['user'].username, self.receiver_username)}"
        
        # Join the room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope['user']  # The user sending the message

        # Save the message to the database
        saved_message = await self.save_message(sender, self.receiver, message)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': saved_message.timestamp.strftime("%b %d %Y, %I:%M %p"),
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp':timestamp
        }))

    @sync_to_async
    def save_message(self, sender, receiver, message):
        from .models import Message

        return Message.objects.create(sender=sender, receiver=receiver, message=message)
