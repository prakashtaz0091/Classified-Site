from django.contrib import admin

from .models import Category, SubCategory, SubCategoryInfo,Field


# Register your models here.
class category_admin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["category_name"],
    }
    list_display = (
        "category_name",
        "slug",
    )


class subcategory(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["category_name"],
    }
    list_display = ("category_name", "slug",)


admin.site.register(Category, category_admin)
admin.site.register(SubCategory, subcategory)
admin.site.register(SubCategoryInfo)
admin.site.register(Field)
