from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.shortcuts import  get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages
from apps.category.models import Category,Field,FieldOptions,FieldExtra
from apps.store.models import  Product,ProductImages
from apps.accounts.models import Account,UserProfile
from apps.Admin.models import SEOSettings
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.auth.hashers import make_password
# Create your views here.


def admin_index(request):
    products=Product.objects.all().order_by('-id')[:5]
    accounts=Account.objects.all().order_by('-id')[:5]
    user_count=accounts.count()
    product_count=products.count()
    print(products,'products')
    context={
        'products':products,
        'accounts':accounts,
        'user_count':user_count,
        'product_count':product_count
    }
    return render(request,'admin1/index.html',context)



def admin_category(request):
    categories=Category.objects.all().order_by('-id')
    context={
        'categories':categories
    }
    return render(request,'admin1/others/categories.html',context)

def sub_category(request,id):
    try:
        category_instance=Category.objects.filter(parent_id=id)
    
    except:
        pass
    
    context={
        'sub_category':category_instance
    }    
    
    
    return render(request,'admin1/others/sub_category.html',context)



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
    fields=Field.objects.all().order_by('-id')
    context={
        'fields':fields
    }
    return render(request,'admin1/list_fields.html',context)



def add_options(request,id):
    linked_to=Field.objects.filter(id=id).first()
    field_options=FieldOptions.objects.filter(linked_to=linked_to).order_by('-id')
    context={
        'options':field_options,
        'id':id
        
    }
   
    return render(request,'admin1/add/add-option.html',context)


def extra_information(request,id):
    linked_to=FieldOptions.objects.filter(id=id).first()
    extras=FieldExtra.objects.filter(linked_to=linked_to).order_by('-id')
    context={
        'id':id,
        'extras':extras
    }
    return render(request,'admin1/add/extra_information.html',context)


def ads(request):
    ads=Product.objects.all().order_by('-id')
    context={
        'ads':ads
    }
    return render(request,'admin1/Ads/ads.html',context)



def ads_delete(request,id):
    try:
        ads=Product.objects.get(id=id)
        ads.delete()
        return redirect('ads')
    
    except:
        pass
    
    
def approved_ads(request,id):
    try:
     
            product=Product.objects.get(id=id)    
            product.is_approved=True
            product.is_available=True
            product.is_rejected=False
            product.save()
            ads=Product.objects.all().order_by('-id')
            context={
                'ads':ads
            }
            return render(request,'admin1/Ads/ads.html',context)

        
    except:
         pass
     
def reject_ads(request,id):
    try:
      
     
            product=Product.objects.get(id=id)    
            product.is_rejected=True
            product.is_approved=False
            product.is_available=False
            product.save()
            ads=Product.objects.all().order_by('-id')
            context={
                'ads':ads
            }
            return render(request,'admin1/Ads/ads.html',context)

        
    except:
         pass
     
     
        
def pending(request):
    product=Product.objects.filter(is_approved=False)
    context={
        'ads':product
        
    }
    return render(request,'admin1/Ads/pending.html',context)



def approve(request):
    ads=Product.objects.filter(is_approved=True).order_by('-id')
    context={
        'ads':ads
    }
    return render(request,'admin1/Ads/approve.html',context)

def reject(request):
    reject_ads=Product.objects.filter(is_rejected=True).order_by('-id')
    context={
        'ads':reject_ads
    }
    return render(request,'admin1/Ads/reject.html',context)

def ads_details(request,slug):
    product=Product.objects.get(slug=slug)
    product_images=ProductImages.objects.filter(product=product)
    context={
        'product':product,
        'product_images':product_images
    }
    return render(request,'admin1/Ads/ads_details.html',context)



def edit_ads(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        print(request.POST,'=======+++>')
        product_name = request.POST.get('product_name')
        subcategory = request.POST.get('subcategory')
        category = request.POST.get('category')
        description = request.POST.get('description')
        price = request.POST.get('price')
        nego = request.POST.get('nego')
        images = request.FILES.getlist('images')
        category=Category.objects.get(id=category)
        subcategory=Category.objects.get(id=subcategory)

        # Update the product's existing fields
        product.product_name = product_name
        product.subcategory = subcategory
        product.category =category
        product.description = description
        product.price = price
        product.negotiable = True if nego == 'on' else False
        
        product.save()

       
        if images:
          
            for image in images:
                ProductImages.objects.create(product=product, image=image)
        
        return redirect('ads')  

    else:
        category = Category.objects.all().order_by('-id')
        context = {
            'product': product,
            'category': category,
            'id': id
        }
        return render(request, 'admin1/Ads/edit_ads.html', context)




def user_list(request):
    users = Account.objects.filter(is_superadmin=True)
    user_statuses = []

    for user in users:
        # Calculate the time since the last login
        if user.last_login:
            time_since_login = now() - user.last_login
        else:
            time_since_login = None

        if user.is_active and time_since_login and time_since_login < timedelta(minutes=5):
            status = 'Online'
        else:
            status = 'Offline'

        user_statuses.append({
            'user': user,
            'status': status,
            'last_login': user.last_login,
            'time_since_login': time_since_login
        })

    context = {
        'user_statuses': user_statuses,
    }
    return render(request,'admin1/user/user_list.html',context)


def add_user(request):
    if request.method == "POST":
        profile_photo = request.FILES.get('profile_photo')
        if not profile_photo:
            profile_photo = 'admin/assets/profile.png'  
        
        
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        active = request.POST.get('active') == 'on'
        role = request.POST.get('role')

        if password == repeat_password:
            # Create the Account
            account = Account.objects.create(
                full_name=name,
                email=email,
                username=username,
                phone_number=phone_number,
                password=make_password(password),  
                is_active=active,
                role=role,
                is_superadmin=True,
                is_staff=True
            )
           
            # Create the UserProfile
            UserProfile.objects.create(
                full_name=name,
                phone_number=phone_number,
                profile_photo=profile_photo,
                email_address=email,
                user=account,
            )
            
            return redirect('user_list')
        else:
            # Redirect back if passwords do not match
            return redirect('add_user')
            
    else:
        # Render the form if not a POST request
        return render(request, 'admin1/user/add_user.html')
    
    
    
    
def users_delete(request,id):
    try:
        account=Account.objects.get(id=id)
        account.delete()
        return redirect('user_list')
    
    except:
        pass    
    
    


def users_edit(request, id):
    account = get_object_or_404(Account, id=id)
    
    if request.method == 'POST':
        # Extract data from the form
        print(request.POST)
        profile_photo = request.FILES.get('profile_photo')
        print(profile_photo)
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        new_password = request.POST.get('new_password')
        role = request.POST.get('role')
        status = request.POST.get('status') == 'on'
        
        if password and password == new_password:
            account.password = make_password(password)
        elif password and password != new_password:
            pass
        
        

        # Update other account fields
        account.full_name = name
        account.username = username
        account.email = email
        account.phone_number = phone_number
        account.role = role
        account.is_active = status
        account.save()

        # Update or create UserProfile
        profile, created = UserProfile.objects.get_or_create(user=account)
        print(profile_photo)
        if profile_photo:
            profile.profile_photo = profile_photo 
        profile.phone_number = phone_number
        profile.full_name = name

        profile.save()

        return redirect('user_list')

    else:
        context = {
            'account': account,
            'id': id,
        }
        return render(request, 'admin1/user/edit_user.html', context)






def customer_list(request):
    accounts=Account.objects.filter(is_superadmin=False).order_by('-id')
    context={
        'accounts':accounts
    }
    return render(request,'admin1/user/customer.html',context)


def add_customer(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        is_active = request.POST.get('active') == 'on'
        is_suspended = request.POST.get('suspend') == 'on'
        profile_photo=request.FILES.get('profile_photo')
        
        if password==repeat_password:
        
            account=Account.objects.create(
                full_name=name,
                username=username,
                email=email,
                phone_number=phone_number,
                password=make_password(password),
                is_active=is_active,
                is_suspended=is_suspended,
                
            )
            profile, created = UserProfile.objects.get_or_create(user=account)
            if profile_photo:
                profile.profile_photo = profile_photo 
            profile.phone_number = phone_number
            profile.full_name = name
            profile.email_address = name
            profile.save()
            return redirect('customers_list')
                
        else:
            
            return render(request,'admin1/user/add_customer.html')   
        
    else:       
        return render(request,'admin1/user/add_customer.html')



def customers_delete(request,id):
    try:
        account=Account.objects.get(id=id)
        account.delete()
        return redirect('customers_list')
        
    except:
        pass
        


def customers_edit(request,id):
    account=get_object_or_404(Account,id=id)
    if request.method=="POST":
        print(request.POST)
        profile_photo = request.FILES.get('profile_photo', None)  
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        status = request.POST.get('status') == 'on' 
       
        
        account.full_name = full_name
        account.username = username
        account.email = email
        account.phone_number = phone_number
        if status:
            account.is_active = status 
            account.is_suspended=False
        else:
            account.is_active=False    
        account.save()
        profile, created = UserProfile.objects.get_or_create(user=account)
        if profile_photo:
            profile.profile_photo = profile_photo 
        profile.phone_number = phone_number
        profile.full_name = full_name
        profile.save()
        
        return redirect('customers_list') 
    else:
        context={
            'account':account,
            'id':id
        }
       
        return render(request,'admin1/user/edit_customer.html',context)
    
    



def active_suspend(request,id):
    account=get_object_or_404(Account,id=id)
    account.is_active=True
    account.save()
    accounts=Account.objects.filter(is_superadmin=False).order_by('-id')
    context={
        'accounts':accounts
    }
    return render(request,'admin1/user/customer.html',context)    


def suspend(request,id):
    account=get_object_or_404(Account,id=id)
    account.is_active=False
    account.save()
    accounts=Account.objects.filter(is_superadmin=False).order_by('-id')
    context={
        'accounts':accounts
    }
    return render(request,'admin1/user/customer.html',context)    




def account_settings(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)


    if request.method == "POST":
      
        
        user.full_name = request.POST.get('name', user.full_name)
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.phone_number=request.POST.get('phone_number', user.phone_number)
        user.save()
        
        
        user_profile.phone_number = request.POST.get('phone_number', user_profile.phone_number)
        user_profile.description = request.POST.get('bio', user_profile.description)
        user_profile.Address = request.POST.get('address', user_profile.Address)
        user_profile.country = request.POST.get('country', user_profile.country)
        user_profile.state = request.POST.get('state', user_profile.state)
        user_profile.city = request.POST.get('city', user_profile.city)
        user_profile.pincode = request.POST.get('pincode', user_profile.pincode)
        user_profile.language = request.POST.get('specialist', user_profile.language)
        
        if request.FILES.get('profile_photo'):
            user_profile.profile_photo = request.FILES['profile_photo']
            
        user_profile.save()
        print('saveed')
        
        return redirect('account_settings')
    
    
    context={
        
        'user':user,
        'userprofile':user_profile
        
    }
        
    return render(request,'admin1/settings/account.html',context)

def password_settings(request):
    
    return render(request,'admin1/settings/security.html')


def change_password(request):
    if request.method == "POST":
        print(request.POST,'data')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect('change_password')
        
        
        
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('change_password')
        
        
        user.set_password(new_password)
        user.save()
        
        update_session_auth_hash(request, user)
        messages.success(request, "Your password has been updated successfully.")
        return redirect('security_settings') 

    return render(request,'admin1/settings/change_password.html')




# for seo 


def seo(request):
    seo=SEOSettings.objects.all().order_by('-id')
    context={
        'seo':seo
    }
    return render(request,'admin1/seo/seo.html',context)




def seo_delete(request,id):
    try:
        
        seo=SEOSettings.objects.get(id=id)
        seo.delete()
        return redirect('seo')
    
    except:
        pass



def seo_edit(request,id):
    seo=SEOSettings.objects.get(id=id)
    if request.method=='POST':
        meta_title=request.POST.get('meta_title')
        site_description=request.POST.get('site_description')
        keywords=request.POST.get('keywords')
        
        seo.meta_title=meta_title
        seo.site_description=site_description
        seo.keywords=keywords
        
        seo.save()
        
        return redirect('seo')
        
    else:
        context={
            'seo':seo
        }
        return render(request,'admin1/seo/edit_seo.html',context)    


def add_seo(request):
    if request.method=='POST':
        print(request.POST)
        page=request.POST.get('page')
        meta_title=request.POST.get('meta_title')
        site_description=request.POST.get('site_description')
        keyword=request.POST.get('keyword')
        
        SEOSettings.objects.create(
            page=page,
            meta_title=meta_title,
            site_description=site_description,
            keywords=keyword
        )
        return redirect('seo')
    return render(request,'admin1/seo/add_seo.html')



    


