from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('service_details/',views.service_details,name='service_details')
]
