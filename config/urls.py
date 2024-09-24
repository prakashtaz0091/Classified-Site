from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


admin.site.site_header = 'Administration'
admin.site.site_title = "Title"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.accounts.urls')),
    path('', include('apps.home.urls')),
    path('jobs/', include('apps.job.urls')),
    path('category/', include('apps.category.urls')),
    path('ad/', include('apps.store.urls')),
    path('', include('apps.contact.urls')),
    path('admins/', include('apps.Admin.urls')),
    path('business_listing/',include('apps.business_listing.urls')),
    path('real-estate/',include('apps.property.urls')),
    path('vechiles/',include('apps.vechiles.urls')),
    path('discover/',include('apps.discover.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
