from django.urls import path
from . import views
urlpatterns=[
    path("",views.landing_page,name="vechile_landing_page"),
    path("filter-vechiles/",views.vechiles_category,name="filter_vechiles"),
]
