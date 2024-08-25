# Create your models here.
from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    descriptions = models.TextField(max_length=255, blank=True)
    category_image = models.FileField(
        upload_to="category/",
        blank=True,
        null=True,
        default="/path/to/default/image.jpg",
    )

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category_name = models.CharField(max_length=1000, unique=True)
    parent = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="sub_categories"
    )
    slug = models.SlugField(max_length=1000, unique=True)
    image=models.FileField(upload_to="sub_category/",blank=True,null=True,default="/path/to/default/image.jpg")
    description=models.CharField(max_length=500,blank=True)

    def __str__(self):
        return self.category_name

class SubCategoryInfo(models.Model):
    #Content titles and content type are used to specify the details that will be used in categories
    content_titles=models.JSONField(blank=True,null=True)
    content_types=models.JSONField(blank=True,null=True)
    category=models.OneToOneField(SubCategory,on_delete=models.CASCADE)
    content_datas=models.JSONField(blank=True,null=True)


