from django.urls import path
from . import views

urlpatterns = [
    # path('category/', views.category_view, name='category'),
    path('<slug:slug>/', views.listing_view, name='listing'),
]