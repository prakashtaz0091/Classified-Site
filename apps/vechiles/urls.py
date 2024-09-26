from django.urls import path
from . import views
urlpatterns=[
    path("",views.landing_page,name="vechile_landing_page")
]
