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
    order=models.IntegerField(blank=True,null=True,default=0)
    
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
            slug_count = Category.objects.filter(slug=self.slug).count()
            if slug_count > 0:
                self.slug = f"{self.slug}-{slug_count + 1}"
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
    # Used to determine if any select types have other fields dependent upon it
    sub_type=models.CharField(null=True,blank=True,max_length=20)
    created_at=models.DateField(auto_now_add=True)
    linked_to=models.ForeignKey(Category,related_name='fields',blank=True,null=True,on_delete=models.CASCADE)

class FieldOptions(models.Model):
    field_value=models.CharField(max_length=255)
    order=models.IntegerField(blank=True,null=True)
    required=models.BooleanField(default=False)
    linked_to=models.ForeignKey(Field,related_name='field_options',on_delete=models.CASCADE,blank=True,null=True)

class FieldExtra(models.Model):
    menu_text=models.CharField(max_length=255)
    mandatory=models.BooleanField(default=False)
    disabled=models.BooleanField(default=False)
    linked_to=models.ForeignKey(FieldOptions,related_name='field_extras',on_delete=models.CASCADE,blank=True,null=True)

class FieldExtraContent(models.Model):
    name=models.CharField(max_length=255)
    order=models.IntegerField(blank=True,null=True,default=1)
    linked_to=models.ForeignKey(FieldExtra,related_name='field_extras_content',on_delete=models.CASCADE,blank=True,null=True)


