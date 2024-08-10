from django.shortcuts import render

# Create your views here. i am your home


def home(request):
    if request.method=='GET':
        return render(request,'home/index.html')