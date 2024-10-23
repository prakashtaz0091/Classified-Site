import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.db.models import  Q


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

        # Get all messages between the current user and the receiver
        messages = await sync_to_async(lambda: list(Message.objects.filter(
            Q(sender=self.scope['user'], receiver=self.receiver) |
            Q(sender=self.receiver, receiver=self.scope['user'])
        ).order_by('timestamp')) )()

        # Process messages into JSON format using sync_to_async
        messages_json = await sync_to_async(self.serialize_messages)(messages)


        
        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_info',
                'receiver': self.receiver.full_name,
                'receiver_profile_photo': await sync_to_async(lambda: self.receiver.profile.profile_photo.url)(),
                'old_messages': messages_json
            }
        )

        

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
                'timestamp': saved_message.timestamp.strftime("%b %d %Y, %I:%M %p"),
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        message = event['message']
        timestamp = event['timestamp']

        await self.send(text_data=json.dumps({

            'type': 'chat_message',
            'message': message,
            'timestamp':timestamp,
        }))



    async def chat_info(self, event):
        # Send the message to WebSocket
        receiver = event['receiver']
        receiver_profile_photo = event['receiver_profile_photo']
        old_messages = event['old_messages']

        await self.send(text_data=json.dumps({
            'type': 'chat_info',
            'receiver': receiver,
            'receiver_profile_photo': receiver_profile_photo,
            'old_messages': old_messages
        }))



    @sync_to_async
    def save_message(self, sender, receiver, message):
        from .models import Message

        return Message.objects.create(sender=sender, receiver=receiver, message=message)





    @staticmethod
    def serialize_messages(messages):
        """Convert messages to JSON format."""
        messages_json = []
        for message in messages:
            messages_json.append({
                'message': message.message,
                'timestamp': message.timestamp.strftime("%b %d %Y, %I:%M %p"),
                'sender': message.sender.username,
                'receiver': message.receiver.username
            })
        return messages_json