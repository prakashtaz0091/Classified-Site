# from django.db import models

# # Create your models here.
# class Property(models.Model):
#     description = models.TextField(blank=True, null=True)  # Optional field for additional property info
#     logo = models.FileField(upload_to='property_logos/', blank=True, null=True)  # Field to upload the property logo
#     property_type = models.CharField(max_length=50,)
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.property_type}"