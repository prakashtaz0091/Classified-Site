from django.urls import path

from . import views

urlpatterns = [
   path("jobs/",views.job,name='job'),
   path("job_category/",views.job_category,name='job_category'),
   
]
