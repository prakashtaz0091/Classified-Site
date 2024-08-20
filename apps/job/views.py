from django.shortcuts import render
from .models import JobCategory,Job
# Create your views here.

def job(request):
    job_category=JobCategory.objects.all()
    job_vacancy=Job.objects.all()
    context={
        'job_category':job_category,
        'job_vacancy':job_vacancy
    }
    return render(request,'home/index-8.html',context)



def job_category(request):
    job_category=JobCategory.objects.all()
    context={
        'job_category':job_category
    }
    return render(request,'others/job_category.html',context)