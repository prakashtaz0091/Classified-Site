from django.shortcuts import render

# Create your views here.


def admin_index(request):
    return render(request,'admin1/index.html')



def admin_category(request):
    return render(request,'admin1/others/categories.html')


def add_category(request):
    return render(request,'admin1/add/add-categories.html')