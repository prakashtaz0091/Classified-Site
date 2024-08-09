from django.shortcuts import render,HttpResponse

# Create your views here.

def account(request):
    return HttpResponse('hello buddy')
