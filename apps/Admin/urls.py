
from django.urls import path
from . import views

urlpatterns = [

    path('index/',views.admin_index,name='admin_index'),
    path('categories/',views.admin_category,name='admin_category'),
    path('add/categories/',views.add_category,name='add_admin_category'),
    path('fields/',views.fields,name='admin_fields'),
    
    
]