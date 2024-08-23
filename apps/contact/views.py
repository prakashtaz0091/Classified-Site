from django.shortcuts import render,redirect
from . models import Contact
# Create your views here.


def contact(request):
    print(request.POST)
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST['message']
        print('contact data has been')
        print(name,email,subject,message)
        
        try:
        
            Contact.objects.create(name=name,
                                email=email,
                                subject=subject,
                                message=message)
        except:
            pass    
        
        
        return redirect('contact')
    
    else:
        print('this is get method')
        return render(request,'company/contact.html')