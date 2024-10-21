from django.contrib import admin
from .models import SEOSettings,SiteSettings,Language,BlogPost,Tag


class SEOSettingsAdmin(admin.ModelAdmin):
    list_display = ('page', 'meta_title', 'site_description', 'keywords')
    search_fields = ('page', 'meta_title')


admin.site.register(SEOSettings,SEOSettingsAdmin)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('paypal_live_mode', 'max_free_ads_expire_days', 'max_free_ads', 'post_ttl', 'max_promotional_mail')
    
    
    
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'order', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'code')    
    
    
admin.site.register(BlogPost)    
admin.site.register(Tag)    