from django.shortcuts import render,HttpResponse

# Create your views here.

def account(request):
    return HttpResponse('hello buddy')



def Login(request):
    return render(request,'accounts/login.html')

def Register(request):
    return render(request,'accounts/signup.html')

def forget_password(request):
    return render(request,'accounts/forgot-password.html')