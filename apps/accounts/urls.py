from django.urls import path
from . import views

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    path('',views.account,name='account')
]
