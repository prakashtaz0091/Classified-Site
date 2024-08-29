
from django.urls import path
from . import views

urlpatterns = [

    path('index/',views.admin_index,name='admin_index'),
    path('categories/',views.admin_category,name='admin_category'),
    path('add/categories/',views.add_category,name='add_admin_category'),
    path('add/subcategory/<category_slug>/',views.add_sub_category,name='add_subcategory'),
    path('fields/',views.fields,name='admin_fields'),
    path('list_fields/',views.list_fields,name='admin_list_fields'),
    path('add_options/<int:id>/',views.add_options,name='add_options'),
    path('extra_information/<int:id>/',views.extra_information,name='extra_information'),
    
    path('list/sub_category/<int:id>/',views.sub_category,name='sub_category'),
    
    
]
