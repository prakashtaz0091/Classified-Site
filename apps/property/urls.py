from django.urls import path
from . import views
urlpatterns=[
    path("",views.landing_page,name="property_landing_page"),
    path("listing_list_sidebar/<slug:slug>",views.listing_list_sidebar,name="listing_list_sidebar")
]
