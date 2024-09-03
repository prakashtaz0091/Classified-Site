from django.contrib import admin
from .models import SEOSettings


class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ('page', 'meta_title', 'site_description', 'keywords')
    search_fields = ('page', 'meta_title')


admin.site.register(SEOSettings,SEOSettingsAdmin)