from django.shortcuts import render,redirect
from . models import Contact
from django.contrib import auth, messages

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
            messages.success(
                request, "Form has been submited sucessfully."
            )
        except:
            pass    
        
        
        return redirect('contact')
    
    else:
        print('this is get method')
        return render(request,'company/contact.html')