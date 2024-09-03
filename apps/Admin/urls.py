
from django.urls import path
from . import views

urlpatterns = [

    path('dashboard/',views.admin_index,name='admin_index'),
    path('categories/',views.admin_category,name='admin_category'),
    path('add/categories/',views.add_category,name='add_admin_category'),
    path('add/subcategory/<category_slug>/',views.add_sub_category,name='add_subcategory'),
    path('fields/',views.fields,name='admin_fields'),
    path('list_fields/',views.list_fields,name='admin_list_fields'),
    path('add_options/<int:id>/',views.add_options,name='add_options'),
    path('extra_information/<int:id>/',views.extra_information,name='extra_information'),
    
    path('list/sub_category/<int:id>/',views.sub_category,name='sub_category'),
    
    # for ads 
    path('ads/',views.ads,name='ads'),
    path('ads/pending/',views.pending,name='pending'),
    path('ads/approve/',views.approve,name='approve'),
    path('ads/reject/',views.reject,name='reject'),
    path('ads/details/<slug:slug>/',views.ads_details,name='ads_details'),
    path('ads/delete/<int:id>/',views.ads_delete,name='ads_delete'),
    path('ads/approve/<int:id>/',views.approved_ads,name='approve_ads'),
    path('ads/reject/<int:id>/',views.reject_ads,name='reject_ads'),
    path('ads/edit/<int:id>/',views.edit_ads,name='edit_ads'),
    
    
    
    # for user 
    
    path('user_list/',views.user_list,name='user_list'),
    path('add_user/',views.add_user,name='add_user'),
    path('user/delete/<int:id>/',views.users_delete,name='users_delete'),
    path('user/edit/<int:id>/',views.users_edit,name='users_edit'),
    
    
    
    # for customers
    
    path('customer_list/',views.customer_list,name='customers_list'),
    path('add_customer/',views.add_customer,name='customers_add'),
    path('customer/delete/<int:id>/',views.customers_delete,name='customers_delete'),
    path('customer/edit/<int:id>/',views.customers_edit,name='customers_edit'),
    
    
    
    # for active and suspend user
    
    path('active_customer/<int:id>/',views.active_suspend,name='active'),
    path('suspend_customer/<int:id>/',views.suspend,name='suspend'),
    
    
    # for account admin settings 
    
    path('account/settings/',views.account_settings,name='account_settings'),
    path('password/settings/',views.password_settings,name='security_settings'),
    path('change_password/',views.change_password,name='change_password'),

    
     
    
    
    
    

    
    

    
]
