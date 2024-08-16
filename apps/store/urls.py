from django.urls import path
from . import views

urlpatterns = [
    path('toggle-bookmark/', views.toggle_bookmark, name='toggle_bookmark'),
    path('service_details/',views.service_details,name='service_details'),
    #add review
    path('add_review/',views.add_review,name="add_review"),
    path('<product_slug>/',views.service_details,name='service_detail'),

    # Will remove this service_details later now required for featured products or home page to be shown
   
    
]
