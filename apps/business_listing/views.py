from django.shortcuts import render

from apps.category.models import Category

# Create your views here.

def list_business_listings(request):
    try:
        industry_standards_instance=Category.objects.filter(industry_standard=True)
        context={
            'businesses':industry_standards_instance
        }
        return render(request,'business_listing/businesses.html',context)
    except Exception as e:
        print(e)
