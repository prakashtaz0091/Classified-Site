from django.urls import path
from . import views

urlpatterns = [
    # path('category/', views.category_view, name='category'),
    path('search/', views.search, name='search'),
    path('<slug:slug>/', views.listing_view, name='listing'),
    
    # path('api/products/', views.get_products, name='get_products'),
]
