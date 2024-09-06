from django.urls import path
from . import views
urlpatterns=[
    path('',views.list_business_listings,name='list business listings'),
]
