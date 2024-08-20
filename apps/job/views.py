from django.shortcuts import render
from .models import JobCategory,Job
from django.db.models import Count



def job(request):
    job_category = JobCategory.objects.annotate(num_jobs=Count('job'))
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




def job_category_listing(request,slug):
    category=JobCategory.objects.filter(slug=slug).first()
    print(category)
    job=Job.objects.filter(category=category)
    print(job,'job')
    context={
        'category':category,
        'jobs':job
    }
    return render(request,'others/job_listing.html',context)



def view_all_jobs(request):
    jobs=Job.objects.all()
    
    context={
        'jobs':jobs
    }
    return render(request,'jobs/all_jobs.html',context)



def search_job(request):
    location = request.GET.get('location', '')
    skills = request.GET.get('skills', '')
    
    
    jobs = Job.objects.all()
    
    if location:
        jobs = jobs.filter(location__icontains=location)
        
    if skills:
        jobs=jobs.filter(title__icontains=skills)
        
        
   
        
    context={
        'jobs':jobs
    }
    
    return render(request,'jobs/search.html',context)