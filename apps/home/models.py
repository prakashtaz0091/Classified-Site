from django.db import models

from apps.accounts.models import Account

# Create your models here.
class Reviews(models.Model):
    created_by=models.ForeignKey(Account,related_name='created_by',on_delete=models.CASCADE)
    reviewed_for=models.ForeignKey(Account,related_name='created_to',on_delete=models.CASCADE)
    rating=models.IntegerField()
    review=models.TextField()
    created_at=models.DateField(auto_now=True)
