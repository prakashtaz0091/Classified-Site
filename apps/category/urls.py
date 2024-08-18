from django.urls import path

from . import views

urlpatterns = [
    # path('category/', views.category_view, name='category'),
    path("filter_category/", views.filter_category, name="filter_category"),
    path("", views.category, name="category"),
    path("<slug:slug>/", views.sub_category_list, name="sub_category"),
    path('subcategory/<slug:subcategory_slug>/', views.listing_view, name='listing'),
    path('all/<slug:subcategory_slug>/', views.viewall_listing_view, name='view_all'),
    # path('sub_categories/<slug:slug>/',views.sub_category_list, name='sub_category'),    
]
