from django.db import models


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