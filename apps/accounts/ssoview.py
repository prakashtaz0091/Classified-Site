import json
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import redirect, render,HttpResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.models import Account
# Create your views here.

@csrf_exempt
def google_login(request):
        try:
            data=json.loads(request.body)
            id_token_data = data['id_token']
            CLIENT_ID = "230604273167-guv4saijfahagueh5kc6ggq01mug2ilv.apps.googleusercontent.com"
            idinfo = id_token.verify_oauth2_token(id_token_data, requests.Request(), CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            # Here you can create a user session or perform any other necessary actions.
            username=idinfo['name']
            email=idinfo['email']
            first_name=idinfo['given_name']
            last_name=idinfo['family_name']
            full_name=f"{first_name} {last_name}"

            account_instance=Account.objects.filter(email=email).first()

            if account_instance is None:
                account_instance=Account(full_name=full_name,email=email,is_active=True)
                account_instance.set_unusable_password() #since password is not needed
                account_instance.save()

            auth.login(request,account_instance)
            
            print(request.user)
            return JsonResponse({
                'status':'success',
                "message": "User login successfully",
                'email':email
                }, status=200)

           
        except Exception as e:
            error=str(e)
            print(error)
            return JsonResponse({'message':f"unexpected error {error}",'status':False},status=400)

@csrf_exempt
def facebook_login(request):
        try:
            data=json.loads(request.body)
            full_name= data.get('name')
            email=data.get('email')
            account=Account.objects.filter(email=email).first()

            if account is  None:
                account=Account(full_name=full_name,email=email,is_active=True)
                account.set_unusable_password() #since password is not needed
                account.save()

            auth.login(request,account)
            print(request.user)
            return JsonResponse({
                'status':'success',
                "message": "User login successfully",
                'email':email
                }, status=200)

           
        except Exception as e:
            error=str(e)
            print(error)
            return JsonResponse({'message':f"unexpected error {error}",'status':False},status=400)

def sso_login(request):
    email=request.POST.get('email')
    account_instance=Account.objects.filter(email=email).first()
    print(request.user)
    auth.login(request,account_instance)
    print(request.user)
    return redirect('/')
