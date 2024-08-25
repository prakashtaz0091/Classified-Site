from django.contrib import admin
from .models import Contact
# Register your models here.
class contactAdmin(admin.ModelAdmin):
    list_display=('name','email','subject')
admin.site.register(Contact,contactAdmin)