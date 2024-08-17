from django.urls import path

from . import views

urlpatterns = [
    # path('category/', views.category_view, name='category'),
<<<<<<< HEAD
    path("search/", views.search, name="search"),
    path("", views.category, name="category"),
    path("<slug:slug>/", views.listing_view, name="listing"),
=======
    # path('search/', views.search_products, name='search'),
    path('',views.category,name='category'),
    path('<slug:slug>/', views.listing_view, name='listing'),
    
>>>>>>> origin/master
    # path('api/products/', views.get_products, name='get_products'),
]
