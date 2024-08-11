from django.db import models
from apps.category.models import Category
from apps.accounts.models import Account
# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=500)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(blank=True)
    images=models.ImageField(upload_to='photos/products')
    price=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    created_by=models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)

    # def get_url(self):
    #     return reverse('product_details',args=[self.category.slug, self.slug])
    
    def __str__(self):
        return self.product_name
