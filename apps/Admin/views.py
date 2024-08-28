from django.http import JsonResponse
from django.shortcuts import render

from apps.category.models import Category

# Create your views here.


def admin_index(request):
    return render(request,'admin1/index.html')



def admin_category(request):
    return render(request,'admin1/others/categories.html')


def add_category(request):
    return render(request,'admin1/add/add-categories.html')

def add_sub_category(request,category_slug):
    try:
        category_instance=Category.objects.filter(slug=category_slug).first()
        if category_instance is None:
            raise Exception("The category u provided is not found")
        context={'category_slug':category_slug}
        return render(request,'admin1/add/add-categories.html',context)
    except Exception as e:
        print(e)
        return JsonResponse({'error':f"unexpected error occured {str(e)}"},status=400)


def fields(request):
    return render(request,'admin1/add/fields.html')



def list_fields(request):
    return render(request,'admin1/list_fields.html')



def add_options(request):
    return render(request,'admin1/add/add-option.html')


def extra_information(request):
    return render(request,'admin1/add/extra_information.html')