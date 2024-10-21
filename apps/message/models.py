from django.db import models
from apps.accounts.models import Account

class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender_messages', blank=True, null=True)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver_messages', blank=True, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"