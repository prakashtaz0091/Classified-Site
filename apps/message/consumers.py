import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.db.models import  Q
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64
from channels.db import database_sync_to_async






@database_sync_to_async
def get_files(saved_message):
    return [{'name': f.file.name, 'url': f.file.url} for f in saved_message.files.all()]

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
        files_data = data.get('files', [])  # List of files attached to the message

        # Save the message to the database
        saved_message = await self.save_message(sender, self.receiver, message, files_data)


        files = await get_files(saved_message)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'receiver': self.receiver.username,
                'timestamp': saved_message.timestamp.strftime("%b %d %Y, %I:%M %p"),
                'files': files,
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        message = event['message']
        timestamp = event['timestamp']

        sender = event['sender']
        receiver = event['receiver']
        files = event.get('files', [])

        await self.send(text_data=json.dumps({

            'type': 'chat_message',
            'message': message,
            'timestamp':timestamp,
            'sender': sender,
            'receiver': receiver,
            'files': files  # Include file URLs if there are any
        }))



    async def chat_info(self, event):
        # Send the message to WebSocket
      
        old_messages = event['old_messages']

        await self.send(text_data=json.dumps({
            'type': 'chat_info',
            
            'old_messages': old_messages
        }))


   

    # @sync_to_async
    async def save_message(self, sender, receiver, message, files_data):
        from .models import Message, MessageFile
        message = await sync_to_async(Message.objects.create)(sender=sender, receiver=receiver, message=message)


        # If there are files, save them
        for file_data in files_data:
            file_name = f"message_files/{file_data['name']}"
            file_content = ContentFile(base64.b64decode(file_data['content']))
            file_path = default_storage.save(file_name, file_content)

            await sync_to_async(MessageFile.objects.create)(
                message=message,
                file=file_path
            )

        return message





    @staticmethod
    def serialize_messages(messages):
        """Convert messages to JSON format."""
        messages_json = []
        for message in messages:
            messages_json.append({
                'message': message.message,
                'timestamp': message.timestamp.strftime("%b %d %Y, %I:%M %p"),
                'sender': message.sender.username,
                'receiver': message.receiver.username,
                'files': [
                    {'name': f.file.name, 'url': f.file.url} for f in message.files.all()
                ]  # Include attached files in the message data
            })
        return messages_json