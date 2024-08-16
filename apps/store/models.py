from django.db import models
from apps.category.models import Category
from apps.accounts.models import Account
from django.utils.text import slugify

class ContactInformation(models.Model):
    email = models.EmailField(blank=True,null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.email}"
    
class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
       
class Location(models.Model):
    Location=models.CharField(max_length=250,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True)
    map_address = models.CharField(max_length=100,blank=True)
    latitude = models.DecimalField(max_digits=100, decimal_places=6,blank=True)
    longitude = models.DecimalField(max_digits=100, decimal_places=6,blank=True)

    def __str__(self):
        return f"{self.address}"


class Product(models.Model):
    product_name=models.CharField(max_length=500)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(blank=True)
    cover_image=models.FileField(upload_to='photos/product_cover')
    tagline=models.TextField(max_length=550,blank=True,null=True)
    price=models.IntegerField()
    is_available=models.BooleanField(default=True)
    features = models.ManyToManyField(Feature, related_name='stores')
    category = models.ManyToManyField(Category, related_name='products')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="product_location" ,blank=True,null=True)
    contact_information = models.ForeignKey(ContactInformation, on_delete=models.CASCADE, related_name="product_contact_information",blank=True,null=True)

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
    
    
    def __str__(self):
        return self.product.product_name


class BookMark(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='bookmark')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bookmark')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.user.full_name} on {self.product.product_name}"


