from django.urls import path
from . import views

urlpatterns = [
    
    path('<product_slug>/',views.service_details,name='service_detail'),

    # Will remove this service_details later now required for featured products or home page to be shown
    path('service_details/',views.service_details,name='service_details')
]
