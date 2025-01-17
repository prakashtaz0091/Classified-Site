from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('landing/',views.landing,name='landing_page'),
    path("privacy/", views.privacy, name="privacy"),
    path("something_wrong/", views.something_wrong, name="error"),
    path("freq_question/", views.freq_question, name="freq_question"),
    path("terms/", views.terms, name="terms"),
    path("how_it_works/", views.how_it_works, name="how_it_works"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("my_listing/", views.my_listing, name="my_listing"),
    path("book_marks/", views.book_marks, name="book_marks"),
    path("messages/", views.messages, name="messages"),
    path("reviews/", views.reviews, name="reviews"),
    path("feedback/<str:hashed_user_id>/", views.feedback, name="customer_feeback"),
    path("add_listing/", views.add_listing, name="add_listing"),
    path(
        "delete_my_listing/<int:id>/", views.delete_my_listing, name="delete_my_listing"
    ),
    path("edit_my_listing/<int:id>/", views.edit_my_listing, name="edit_my_listing"),
 
    
    path('',views.home,name='home'),
    path('privacy/',views.privacy,name='privacy'),
    path('something_wrong/',views.something_wrong,name='error'),

    path('freq_question/',views.freq_question,name='freq_question'),
    path('terms/',views.terms,name='terms'),
  
    path('search/',views.search,name='search'),
    path('how_it_works/',views.how_it_works,name='how_it_works'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('all_ads/',views.all_ads,name='all_ads'),
   
    path('my_listing/',views.my_listing,name='my_listing'),
    path('book_marks/',views.book_marks,name='book_marks'),
    path('messages/',views.messages,name='messages'),
    path('reviews/',views.reviews,name='reviews'),
    path('feedback/<str:hashed_user_id>/',views.feedback,name='customer_feeback'),
    path('add_listing/',views.add_listing,name='add_listing'),
    path('delete_my_listing/<int:id>/',views.delete_my_listing,name='delete_my_listing'),
    path('edit_my_listing/<int:id>/',views.edit_my_listing,name='edit_my_listing'),
    
    
    
    # for subcategory 
    
    path('sub_category/',views.sub_category,name='sub_category'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'), 
    path('banner/', views.banner, name='banner'),
    path('add/banner/', views.add_banner, name='add_banner'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('backup/', views.backup, name='backup'),
]
