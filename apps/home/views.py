from django.shortcuts import render

# Create your views here. i am your home


def home(request):
    if request.method=='GET':
        return render(request,'home/index.html')
    
    
def service_details(request):
    return render(request,'home/service-details.html')    