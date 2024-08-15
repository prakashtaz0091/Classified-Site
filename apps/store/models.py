from django.db import models
from apps.category.models import Category
from apps.accounts.models import Account
from django.utils.text import slugify


class Product(models.Model):
    product_name=models.CharField(max_length=500)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(blank=True)
    cover_image=models.FileField(upload_to='photos/product_cover')
    price=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name="product_category")
    created_date=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    view_count=models.IntegerField(default=0)
    created_by=models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name

class ProductImages(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.FileField(upload_to="photos/products")


class BookMark(models.Model):
   

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='bookmark')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookmark')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.user.full_name} on {self.product.product_name}"
