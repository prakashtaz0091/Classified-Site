from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True);
    slug=models.SlugField(max_length=100,unique=True)
    descriptions=models.TextField(max_length=255,blank=True);
    category_image=models.FileField(upload_to="category/")

    class Meta:
        verbose_name_plural = "categories"
        
    # def get_url(self):
    #     return reverse('product_by_category',args=[self.slug]) 
    def __str__(self):
      return self.category_name

class SubCategory(models.Model):
    category_name=models.CharField(max_length=1000,unique=True)
    parent=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_categories')
    slug=models.SlugField(max_length=1000,unique=True)
