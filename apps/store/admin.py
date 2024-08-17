from django.contrib import admin

from .models import (BookMark, ContactInformation, Feature, Location, Product,
                     ProductImages)

# Register your models here.


class Store_Admin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["product_name"],
    }
    list_display = ("product_name", "price", "modified_at", "is_available")
    list_display_links = ("product_name", "price", "modified_at", "is_available")


admin.site.register(Product, Store_Admin)
admin.site.register(ProductImages)
admin.site.register(Location)
admin.site.register(ContactInformation)
admin.site.register(Feature)


admin.site.register(BookMark)
