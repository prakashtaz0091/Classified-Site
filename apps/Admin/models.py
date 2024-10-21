from django.db import models
from apps.accounts.models import Account

class SEOSettings(models.Model):
    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('contact', 'Contact Page'),
        ('registration', 'Registration Page'),
        ('about', 'About Us Page'),
        ('services', 'Services Page'),
        ('blog', 'Blog Page'),
        ('faq', 'FAQ Page'),
      
    ]
    page = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True)
    meta_title = models.CharField(max_length=255,help_text="Title that appears in the browser tab and search engines.")
    site_description = models.TextField(help_text="A brief description of the page content, used by search engines.")
    keywords = models.TextField(help_text="A comma-separated list of keywords relevant to the page.")
    created_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meta_title


class SiteSettings(models.Model):
    profile_picture = models.ImageField(upload_to='images/profile_pictures/', blank=True, null=True)
    product_image = models.ImageField(upload_to='images/product_images/', blank=True, null=True)
    watermark_image = models.ImageField(upload_to='images/watermarks/', blank=True, null=True)
    paypal_live_mode = models.BooleanField(default=False)
    max_free_ads_expire_days = models.IntegerField(default=1, help_text="Maximum number of days before free ads expire.")
    max_free_ads = models.IntegerField(default=3, help_text="Maximum number of free ads allowed.")
    post_ttl = models.IntegerField(default=100, help_text="Time to live for a post, in days.")
    max_promotional_mail = models.IntegerField(default=2, help_text="Maximum number of promotional emails that can be sent.")

    def __str__(self):
        return "Site Settings"

class Language(models.Model):
    LANGUAGE_STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100) 
    code = models.CharField(max_length=10)
    order = models.IntegerField() 
    status = models.CharField(max_length=10, choices=LANGUAGE_STATUS_CHOICES, default='active') 
    created_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
    
    
    
# for blog
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    
class BlogPost(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    created_at = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='blog_posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive')

    def __str__(self):
        return self.title
   
    
