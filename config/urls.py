from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


admin.site.site_header = 'Administration'
admin.site.site_title = "Title"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('apps.accounts.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
