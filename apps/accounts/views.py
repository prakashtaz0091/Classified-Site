from django.shortcuts import render,HttpResponse,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import  urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib import messages,auth
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.decorators import login_required
# Create your views here.

def account(request):
    return HttpResponse('hello buddy')



def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('home')
           
    return render(request,'accounts/login.html')

def Register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if the email already exists
            if Account.objects.filter(email=email).exists():
                messages.error(request, 'Email address is already registered.')
                return render(request, 'accounts/signup.html')
            
            full_name = form.cleaned_data['full_name']
            password = form.cleaned_data['password']
            
            user = Account.objects.create_user(full_name=full_name, email=email, password=password)
            user.save()

            # Send verification email (if required)
            # current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message = render_to_string('accounts/account_verification_email.html', {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            
            messages.success(request, f'Thank you for registering with us. We have sent you a verification email to your email address {email}. Please verify it.')
            return redirect('register')
        else:
            messages.error(request, 'Email address is already registered.')

    else:
        print('i am gt')
        pass
        
    return render(request, 'accounts/signup.html')



def forget_password(request):
    return render(request,'accounts/forgot-password.html')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')
