from django.contrib import admin

from .models import ProductReview, Reviews

# Register your models here.

admin.site.register(Reviews)
admin.site.register(ProductReview)
