from django.urls import path

from . import views

urlpatterns = [
    # path('category/', views.category_view, name='category'),
    path('create_new/',views.create_category,name='create_category'),
    path('create_field/',views.create_field,name='create_field'),
    path('create_field_options/',views.create_field_options,name='create_field_options'),
    path("filter_category/", views.filter_category, name="filter_category"),
    path("filter_sub_category/", views.filter_sub_category, name="filter_sub_category"),
    path("", views.category, name="category"),
    path('subcategory/<slug:subcategory_slug>/', views.listing_view, name='listing'),
    path('all/<slug:subcategory_slug>/', views.viewall_listing_view, name='view_all'),
    path('create_category_info/',views.create_category_info,name='create_category_info'),
    path("<slug:slug>/", views.sub_category_list, name="sub_category"),
    # path('sub_categories/<slug:slug>/',views.sub_category_list, name='sub_category'),    

]
