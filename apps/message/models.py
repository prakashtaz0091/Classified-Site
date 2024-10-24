from django.db import models
from apps.accounts.models import Account

class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender_messages', blank=True, null=True)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver_messages', blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"
    



class MessageFile(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to='message_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File attached to message {self.chat_message.id} on {self.uploaded_at}"