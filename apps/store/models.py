from django.db import models
from django.utils.text import slugify

from apps.accounts.models import Account
from apps.category.models import Category


class ContactInformation(models.Model):
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.email}"


class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    Location = models.CharField(max_length=250, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    map_address = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=100, decimal_places=6, blank=True)
    longitude = models.DecimalField(max_digits=100, decimal_places=6, blank=True)

    def __str__(self):
        return f"{self.address}"


class Product(models.Model):
    product_name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    cover_image = models.FileField(upload_to="photos/product_cover")
    tagline = models.TextField(max_length=550, blank=True, null=True)
    price = models.IntegerField()
    is_available = models.BooleanField(default=False)
    featured_data=models.JSONField(blank=True,null=True)
    features = models.ManyToManyField(Feature, related_name="stores")
    category=models.ForeignKey(Category,related_name='category_products',on_delete=models.CASCADE,blank=True,null=True)
    subcategory=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True,related_name='products')
    negotiable=models.BooleanField(default=False)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="product_location",
        blank=True,
        null=True,
    )
    contact_information = models.ForeignKey(
        ContactInformation,
        on_delete=models.CASCADE,
        related_name="product_contact_information",
        blank=True,
        null=True,
    )

    created_date = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    is_approved=models.BooleanField(default=False)
    is_rejected=models.BooleanField(default=False)
    created_by = models.ForeignKey(
        Account, on_delete=models.CASCADE, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create the initial slug
            initial_slug = slugify(self.product_name)
            # Save the object to generate the ID
            super(Product, self).save(*args, **kwargs)
            # Now that the ID is available, append it to the slug
            self.slug = f"{initial_slug}-{self.id}"
            # Save the object again with the updated slug
            self.save(update_fields=['slug'])
        else:
            super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to="photos/products")

    def __str__(self):
        return self.product.product_name


class BookMark(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="bookmark")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="bookmark"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.user.email} - {self.user.full_name} on {self.product.product_name}"
        )

class FeatureDataImage(models.Model):
    product=models.ForeignKey(Product,related_name='features_images',on_delete=models.CASCADE)
    featured_data_image=models.FileField(blank=True,null=True)
    feature_data_name=models.CharField(max_length=255)


class BannerAds(models.Model):
    POSITION_CHOICES = [
        ('homepage_carousel', 'Homepage Carousel'),
        ('category_page_top', 'Category Page Top Banner'),
        ('homepage_top', 'Homepage Top Banner'),
        ('homepage_bottom', 'Homepage Bottom Banner'),
    ]
    title=models.CharField(max_length=200)
    link=models.URLField()
    price=models.FloatField()
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    city=models.CharField(max_length=100)
    image=models.FileField(upload_to='banner/',null=True)
    
    # only for category banner ads
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='banner_category',blank=True,null=True)
    sub_category=models.ForeignKey(Category,related_name='banner_subcategory',on_delete=models.CASCADE,blank=True,null=True)


class DefaultBannerAdsPricing(models.Model):
    POSITION_CHOICES = [
        ('homepage_carousel', 'Homepage Carousel'),
        ('category_page_top', 'Category Page Top Banner'),
        ('homepage_top', 'Homepage Top Banner'),
        ('homepage_bottom', 'Homepage Bottom Banner'),
    ]
    
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, unique=True)
    description=models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.position} - AED {self.price_per_day} per day'
