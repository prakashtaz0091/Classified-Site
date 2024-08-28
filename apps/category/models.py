# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from datetime import date

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    menu_text=models.CharField(max_length=50,blank=True,null=True)
    slug = models.SlugField(max_length=100, unique=True)
    order=models.IntegerField(blank=True,null=True)
    
    #either classified or job listing like that(choices are not used because it will be posted from limited place)
    category_type=models.CharField(max_length=20,blank=True,null=True)
    menu_item=models.BooleanField(default=False)
    popular_item=models.BooleanField(default=False)
    featured_item=models.BooleanField(default=False)
    latest_item=models.BooleanField(default=False)
    industry_standard=models.BooleanField(default=False)

    # determine the type of media to be used
    media_type=models.CharField(max_length=20,blank=True,null=True)
    long_description=models.TextField(blank=True,null=True)
    short_description=models.TextField(blank=True,null=True)
    #will later add choices to this status
    status=models.CharField(max_length=20,default="ACTIVE")

    meta_title_country=models.CharField(max_length=100,blank=True,null=True)
    meta_description_country=models.TextField(blank=True,null=True)
    meta_keywords_country=models.CharField(max_length=500,blank=True,null=True)

    #Here let city represents both city and country 
    meta_title_city=models.CharField(max_length=100,blank=True,null=True)
    meta_description_city=models.TextField(blank=True,null=True)
    meta_keywords_city=models.CharField(max_length=500,blank=True,null=True)

    #determines whether it is category or not says id but points to entire category just naming 
    parent_id = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )


    category_icon_image = models.FileField(
        upload_to="category/icon/",
        blank=True,
        null=True,
        default="/path/to/default/image.jpg",
    )
    category_thumbnail_image=models.FileField(upload_to='category/thumbnail/',blank=True,null=True)
    created_at=models.DateField(auto_now_add=True,blank=True,null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name

#Named after its name in admin page (Anyway directly points to category)
class Field(models.Model):
    field_name=models.CharField(max_length=255)
    field_type=models.CharField(max_length=40)
    mandatory=models.BooleanField()
    searchable=models.BooleanField()
    featured_style=models.CharField(max_length=30)
    #should have been foreign key but stored in char in adjeem
    hint=models.CharField(max_length=500)
    #Just for showing to admin no actual purpose other than that
    admin_hint=models.CharField(max_length=500)
    icon=models.FileField(upload_to='category/fields/icon/',null=True,blank=True)
    linked_to=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True) #wont be null but still during create it may give issues so
    created_at=models.DateField(auto_now_add=True)

class FieldOptions(models.Model):
    field_value=models.CharField(max_length=255)
    order=models.IntegerField(blank=True,null=True)
    required=models.BooleanField(default=False)
    linked_to=models.ForeignKey(Field,on_delete=models.CASCADE,blank=True,null=True)

class FieldExtra(models.Model):
    menu_text=models.CharField(max_length=255)
    mandatory=models.BooleanField()
    disabled=models.BooleanField()
    linked_to=models.ForeignKey(FieldOptions,on_delete=models.CASCADE,blank=True,null=True)

class FieldExtraContent(models.Model):
    name=models.CharField(max_length=255)
    order=models.IntegerField(blank=True,null=True,default=1)
    linked_to=models.ForeignKey(FieldExtra,on_delete=models.CASCADE,blank=True,null=True)



## Will later remove these models only keeping it now temporarily
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


