from django.urls import path

from . import views

urlpatterns = [
   path("",views.landing_page,name='job_landing_page'),
   path("job_category/",views.job_category,name='job_category'),
   path("all_jobs/",views.view_all_jobs,name='all_jobs'),
   path("search_jobs/",views.search_job,name='search_job'),
   path("job_details/<slug:slug>/",views.job_details,name='job_details'),
   path("jobs/<slug:slug>/",views.job_category_listing,name='job_category_listing'),
   
]
