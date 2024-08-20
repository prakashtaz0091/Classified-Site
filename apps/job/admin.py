from django.contrib import admin
from apps.job.models import JobCategory,Job
# Register your models here.


class jobCategoryAdmin(admin.ModelAdmin):
    
    prepopulated_fields = {
        "slug": ["name"],
    }
    list_display=['name','available_jobs',]
    
    
    
class jobAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ["title"],
    }
    list_display=['title','company_name','location','posted_date']

admin.site.register(JobCategory,jobCategoryAdmin)
admin.site.register(Job,jobAdmin)