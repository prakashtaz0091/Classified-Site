
from django.urls import path
from . import views

urlpatterns = [

   path('dashboard/',views.admin_index,name='admin_index'),
    
    
    # for category 
   path('categories/',views.admin_category,name='admin_category'),
   path('add/categories/',views.add_category,name='add_admin_category'),
   path('add/subcategory/fields/<int:id>/',views.subcategory_fields,name='add_subcategory_fields'),
   path('delete/subcategory/fields/',views.delete_subcategory_fields,name='delete_subcategory_fields'),
   path('add/subcategory/<slug:category_slug>/',views.add_sub_category,name='add_subcategory'),
   path('delete/category/<int:id>/',views.delete_category,name='delete_category'),
   path('edit/category/<int:id>/',views.edit_category,name='edit_category'),
    
    
    
    # for fields 
    
    
    path('add_fields/',views.fields,name='admin_fields'),
    path('delete/fields/<int:id>/',views.delete_fields,name='delete_fields'),
    path('edit/fields/<int:id>/',views.edit_fields,name='edit_fields'),
    path('list_fields/',views.list_fields,name='admin_list_fields'),
    path('add_options/<int:id>/',views.add_options,name='add_options'),
    path('extra_information/<int:id>/',views.extra_information,name='extra_information'),
    path('list/sub_category/<int:id>/',views.sub_category,name='sub_category'),
    
   #  for enable and disable adding extra and extra data
    path('toggle-option/',views.toggle_option_view, name='toggle_option_view'),
    
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
    
    
    # for SEO
    
    path('seo-page/',views.seo,name='seo'),
    path('seo-delete/<int:id>/',views.seo_delete,name='seo_delete'),
    path('seo-edit/<int:id>/',views.seo_edit,name='seo_edit'),
    path('add_seo/',views.add_seo,name='add_seo'),



    # for default settings 
    path('default_settings/',views.default_settings,name='default_settings'),
    path('default-edit/<int:id>/',views.default_edit,name='default_edit'),




   # for languagae
   
   path('languages/',views.language,name='language'),   
   path('languages/delete/<int:id>/',views.delete_language,name='delete_language'),
   path('languages/edit/<int:id>/',views.edit_language,name='edit_language'),
   
   
   
#    for toggle 
   path('fields/required/',views.toggle_field_required, name='toggle-required'),
   path('backup/',views.backup_templates, name='backup'),
   
   
   #for options extra content show model
   path('update-category-url/',views.update_category, name='update-category'),
   path('get-extra-data-url/<int:id>/',views.get_category_data, name='get-category-data'),
   path('fields/show_data/',views.show_view, name='show_data'),
   path('fields/update_data/',views.update_view, name='update_data'),
   path('delete/show_data/',views.delete_show_data, name='delete_show_data'),
   path('delete/extra_information/<int:id>/',views.delete_extra_information, name='delete_extra_information'),
   path('delete/field_options/<int:id>/',views.delete_field_options, name='delete_field_options'),
   path('edit/options/<int:id>/',views.edit_options, name='edit_options'),
   
   #For banners   
   path('banner_ads/listing/',views.list_banner_ads,name="list_banner_ads"),
   path('banner_ads/change_status/',views.change_banner_ads_status,name="change_banner_ads_status"),
   path('banner_ads/create/',views.create_banner_ads,name='create_banner_ads'),
   path('banner_ads/edit/',views.edit_banner_ad,name='edit_banner_ads'),
   path('banner_ads/delete/',views.delete_banner_ad,name='delete_banner_ad'),
   
   
   
   # for pages
   
   path('add_pages/',views.add_pages,name='add_pages') ,
   path('page_list',views.page_list,name='page_list'),
   
   # for blog
   path('all_blogs/',views.all_blogs,name='all_blogs') ,
   path('add_blogs/',views.add_blogs,name='add_blogs') ,
   path('blog_categories/',views.blog_categories,name='blog_categories') ,
   path('blog_comment/',views.blog_comment,name='blog_comment') ,
   
]
