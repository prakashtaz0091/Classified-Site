from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.home,name='home'),
    path('privacy/',views.privacy,name='privacy'),
    path('freq_question/',views.freq_question,name='freq_question'),
    path('terms/',views.terms,name='terms'),
    path('contact/',views.contact,name='contact'),
    path('how_it_works/',views.how_it_works,name='how_it_works'),
    path('dashboard/',views.dashboard,name='dashboard'),
   
    path('my_listing/',views.my_listing,name='my_listing'),
    path('book_marks/',views.book_marks,name='book_marks'),
    path('messages/',views.messages,name='messages'),
    path('reviews/',views.reviews,name='reviews'),
    path('feedback/<str:hashed_user_id>/',views.feedback,name='customer_feeback'),
]
