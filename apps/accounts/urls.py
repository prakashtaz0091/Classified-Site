from django.urls import path
from . import views

urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    # path('',views.account,name='account'),
    path('login/',views.Login,name='login'),
    path('register/',views.Register,name='register'),
    path('forget_password/',views.forget_password,name='forget_password'),
    path('logout/',views.logout,name='logout'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),    
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    # path('change_password/', views.change_password, name='change_password'),
]
