from django.db import models

# Create your models here.


class Contact(models.Model):
    name=models.CharField(blank=True,max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
    
    
    
    
    def __str__(self):
        return f'{self.name} &{self.email}'