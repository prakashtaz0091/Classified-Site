from django.urls import path
from . import views

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    path('',views.account,name='account'),
    path('login/',views.Login,name='login'),
    path('register/',views.Register,name='register'),
    
]
