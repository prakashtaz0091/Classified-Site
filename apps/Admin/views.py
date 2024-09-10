from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.shortcuts import  get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from apps.category.models import Category,Field,FieldOptions,FieldExtra,FieldExtraContent
from apps.store.models import  BannerAds, DefaultBannerAdsPricing, Product,ProductImages
from apps.accounts.models import Account,UserProfile
from apps.Admin.models import SEOSettings,SiteSettings,Language
from django.utils.timezone import now
from datetime import timedelta
from django.urls import reverse
import json
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
    return render(request,'admin1/category/categories.html',context)



def delete_category(request,id):
    category=get_object_or_404(Category,id=id)
    try:
        category.delete()
        return redirect('admin_category')
    except:
        pass
    
    
    
def edit_category(request,id):
    category=get_object_or_404(Category,id=id)
    if request.method=='POST':
        if request.method == 'POST':
        # Extract data from the request
            category_name = request.POST.get('category_name')
            menu_text = request.POST.get('menu_text')
            order = request.POST.get('order')
            type = request.POST.get('type')
            menu_item = request.POST.get('menu_item') == 'yes'
            popular_item = request.POST.get('popular_item') == 'yes'
            featured_item = request.POST.get('featured_item') == 'yes'
            latest_item = request.POST.get('latest_item') == 'yes'
            industry_category = request.POST.get('industry_category') == 'yes'
            media_type = request.POST.get('media_type')
            long_description = request.POST.get('long_description')
            short_description = request.POST.get('short_description')
            status = request.POST.get('status')
            meta_title_country = request.POST.get('meta_title_country')
            meta_description_country = request.POST.get('meta_description_country')
            meta_keywords_country = request.POST.get('meta_keywords_country')
            meta_title_city = request.POST.get('meta_title_city')
            meta_description_city = request.POST.get('meta_description_city')
            meta_keywords_city = request.POST.get('meta_keywords_city')

            # Handling file uploads (icon_image and thumbnail_image)
            icon_image = request.FILES.get('icon_image')
            thumbnail_image = request.FILES.get('thumbnail_image')
            
            
             # Update the category object with the extracted data
            category.category_name = category_name
            category.menu_text = menu_text
            category.order = order
            category.category_type = type
            category.menu_item = menu_item
            category.popular_item = popular_item
            category.featured_item = featured_item
            category.latest_item = latest_item
            category.industry_standard = industry_category
            category.media_type = media_type
            category.long_description = long_description
            category.short_description = short_description
            category.status = status
            category.meta_title_country = meta_title_country
            category.meta_description_country = meta_description_country
            category.meta_keywords_country = meta_keywords_country
            category.meta_title_city = meta_title_city
            category.meta_description_city = meta_description_city
            category.meta_keywords_city = meta_keywords_city
            
             # Only update the images if new ones were uploaded
            if icon_image:
                category.category_icon_image = icon_image
            if thumbnail_image:
                category.category_thumbnail_image= thumbnail_image
            
            category.save()

            # Redirect to a success page or back to the category list
            return redirect('admin_category')    
    else:
        context={
            'category':category,
            'id':id
        }
        return render(request,'admin1/category/edit-category.html',context)    
    
    
    
    
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
    return render(request,'admin1/category/add-categories.html')

def add_sub_category(request,category_slug):
    try:
        category_instance=Category.objects.filter(slug=category_slug).first()
        if category_instance is None:
            raise Exception("The category u provided is not found")
        context={'category_slug':category_slug}
        return render(request,'admin1/category/add-categories.html',context)
    except Exception as e:
        print(e)
        return JsonResponse({'error':f"unexpected error occured {str(e)}"},status=400)


def fields(request):
    return render(request,'admin1/fields/fields.html')



def list_fields(request):
    fields=Field.objects.all().order_by('-id')
    context={
        'fields':fields
    }
    return render(request,'admin1/fields/list_fields.html',context)


def edit_fields(request,id):
    field=get_object_or_404(Field,id=id)
    if request.method=='POST':
        field_name = request.POST.get('field_name')
        field_type = request.POST.get('field_type')
        mandatory = request.POST.get('mandatory') == 'yes'
        searchable = request.POST.get('searchable') == 'yes'
        featured_style = request.POST.get('featured_style')
        hint = request.POST.get('hint')
        admin_hint = request.POST.get('admin_hint')
        icon=request.FILES.get('field_icon')
        
        field.field_name=field_name
        field.field_type=field_type
        field.mandatory=mandatory
        field.searchable=searchable
        field.featured_style=featured_style
        field.hint=hint
        field.admin_hint=admin_hint
        
        if icon:
            field.icon=icon
        
        field.save()
        return redirect('admin_list_fields')    
    
    else:
        context={
            'field':field,
            'id':id 
        }
        return render(request,'admin1/fields/edit_field.html',context)

def delete_fields(request,id):
    field=get_object_or_404(Field,id=id)
    try:
        field.delete()
        return redirect('admin_list_fields')
    
    except:
        pass


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
    users = Account.objects.filter(Q(is_superadmin=True) | Q(is_staff=True)) 
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
            # account = Account.objects.create(
            #     full_name=name,
            #     email=email,
            #     username=username,
            #     phone_number=phone_number,
            #     password=make_password(password),  
            #     is_active=active,
            #     role=role,
            #     is_superadmin=True,
            #     is_staff=True
            # )
           
            account=Account()
            account.full_name=name
            account.email=email
            account.username=username
            account.password=make_password(password)
            account.is_active=active
            account.role=role
            if account.role == 'Admin' or account.role == "Super Admin":
                print('i am in')
                is_superadmin=True 
            
            else:
                print('i am out')
                is_staff=True  
            
            account.save()       
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
    accounts = Account.objects.filter(Q(is_superadmin=False) | Q(is_staff=False))  
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
                is_verify=True
                
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





# for settings 

def default_settings(request):
    seo=SiteSettings.objects.all().order_by("-id")[:1]
    seo
    for seo in seo:
        seo=seo
        
    context={
        'seo':seo 
    }
    return render(request,'admin1/settings/default.html',context)
    


def default_edit(request,id):
    default_settings=get_object_or_404(SiteSettings,id=id)
    if request.method=='POST':
        max_free_ads_expire_days = request.POST.get('max_free_ads_expire_days')
        max_free_ads = request.POST.get('max_free_ads')
        post_ttl = request.POST.get('post_ttl')
        max_promotional_mail = request.POST.get('max_promotional_mail')
        paypal_mode=request.POST.get('paypal_mode')

        
         # Extract image files from request.FILES
        profile_image = request.FILES.get('profle')
        print(profile_image,'profile image')
        product_image = request.FILES.get('product')
        watermark_image = request.FILES.get('watermark')
        
        
        default_settings.max_free_ads=max_free_ads
        default_settings.max_free_ads_expire_days=max_free_ads_expire_days
        default_settings.post_ttl=post_ttl
        default_settings.max_promotional_mail=max_promotional_mail
        
        if profile_image:   
            default_settings.profile_picture=profile_image
            
        if product_image:    
            default_settings.product_image=product_image
        
        if watermark_image:    
            default_settings.watermark_image=watermark_image
        
        default_settings.paypal_live_mode=True if paypal_mode == 'on' else False
        
        
        default_settings.save()
        
        return redirect('default_settings')
        
        
    
    else:
        context={
            'id':id,
            'default_settings':default_settings
        }
        return render(request,'admin1/settings/edit_default.html',context)


    


# for languages 


def language(request):
    language=Language.objects.all().order_by('-id')
    context={
        'languages':language
    }
    return render(request,'admin1/language/language.html',context)


def delete_language(request,id):
    try:
        language=Language.objects.get(id=id)
        language.delete()
        return redirect('language')
    
    except:
        pass



def edit_language(request,id):
    language=get_object_or_404(Language,id=id)
    if request.method == "POST":
        name=request.POST.get('name')
        code=request.POST.get('code')
        order=request.POST.get('order')
        status=request.POST.get('status')
        
        language.name=name
        language.code=code
        language.order=order
        language.status=status
        language.save()
        
        return redirect('language')
        
    else:
        context={
            'language':language,
            'id':id
        }
        return render(request,'admin1/language/edit_language.html',context)    


@csrf_exempt
def toggle_field_required(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id=data.get('option_id')
        is_required=data.get('is_required')
        field_option=FieldOptions.objects.get(id=id)
        field_option.required=is_required
        field_option.save()
      
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)




def backup_templates(request):
    if request.method == "POST":
        print(request.POST)
    context={
        'id':1
    }
    return render(request,'admin1/add/backup.html',context)





# for disbale and mandtory in the extra extra informations 

@csrf_exempt
def toggle_option_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        option_id = data.get('option_id')
        toggle_type = data.get('toggle_type')
        is_checked = data.get('is_checked')
        
        print('data,data',data)

        # Update the relevant option in the database
        try:
            option = FieldExtra.objects.get(id=option_id)
            if toggle_type == 'disabled':
                option.disabled= is_checked
            elif toggle_type == 'mandatory':
                option.mandatory = is_checked
            option.save()
            return JsonResponse({'status': 'success'})
        except FieldExtra.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Option not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def show_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id')
        field_extra=FieldExtra.objects.get(id=id)
        field_extra_content=FieldExtraContent.objects.filter(linked_to=field_extra)
        field_extra_content_list = list(field_extra_content.values()) 
        print(field_extra_content_list)
        return JsonResponse({'status': 'success','data':field_extra_content_list})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    
@csrf_exempt
def update_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print('data',data)
        id=data.get('id')
        
        field_extra_content=FieldExtraContent.objects.get(id=id)
        field_extra_content.name=data.get('name')
        field_extra_content.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def delete_show_data(request):
    if request.method == 'DELETE':
        try:
            if request.body:
                data = json.loads(request.body)
                id=data.get('id')
                field_extra=FieldExtraContent.objects.get(id=id)
                field_extra.delete()
                return JsonResponse({'status': 'success', 'message': 'Data deleted successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No data provided in request body.'}, status=400)
        except json.JSONDecodeError as e:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)





def delete_extra_information(request, id):
    if request.method == 'POST':
        try:
            main_id = request.POST.get('extra_data') 
            field = FieldExtra.objects.get(id=id)
            field.delete()
            return redirect(reverse('extra_information', kwargs={'id': main_id}))
        
        except FieldExtra.DoesNotExist:
            return HttpResponseBadRequest("FieldExtra not found.")
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {str(e)}")
    else:
        return HttpResponseBadRequest("Invalid request method.")
    
    
    
    
def get_category_data(request, id):
    try:
        category = FieldExtra.objects.get(id=id)
       
        data = {
            'success': True,
            'category': {
                'id': category.id,
                'name': category.menu_text,
            }
            
        }
        
        print(data)
    except Category.DoesNotExist:
        data = {'success': False, 'error': 'Category not found'}
    
    return JsonResponse(data)    

@csrf_exempt
def update_category(request):
    if request.method == 'POST':
        print(request.POST)
        category_id = request.POST.get('category_id')
        category_name = request.POST.get('category_name')
        
        try:
            category = FieldExtra.objects.get(id=category_id)
            category.menu_text = category_name
            # Update other fields as necessary
            category.save()

            return JsonResponse({'success': True, 'message': 'extra information updated successfully!'})
        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'extra not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})




def delete_field_options(request, id):
    try:
        main_id = request.POST.get('main_id')
        print(main_id)
        field_options = get_object_or_404(FieldOptions, id=id)
        field_options.delete()
        return redirect(reverse('add_options', kwargs={'id': main_id}))
    
    except FieldOptions.DoesNotExist:
        pass
    
    except Exception as e:    
        print(f"An error occurred: {e}")
   
        
        

def edit_options(request,id):
    option=get_object_or_404(FieldOptions,id=id)
    if request.method == "POST":
        field_value=request.POST.get('field_value')        
        order=request.POST.get('order')
        main_id=request.POST.get('main_id')
        option.field_value=field_value
        option.order=order
        option.save()
        return redirect(reverse('edit_options', kwargs={'id': main_id}))
    
    else:
        context={
            'option':option,
            'id':id
        }
        
        return render(request,'admin1/fields/edit_option.html',context)



#For banner listing
def list_banner_ads(request):
    banner_ads_instance = BannerAds.objects.all()
    context={
        'banner_ads':banner_ads_instance
    }
    print(context)
    return render(request,'admin1/banner_ads/banner_ads.html',context)

#For banner listing
def change_banner_ads_status(request):
    try:
        banner_id=request.GET.get('banner_id')
        status=request.GET.get('status')
        banner_ads_instance = BannerAds.objects.filter(id=banner_id).first()
        banner_ads_instance.status=status
        banner_ads_instance.save()
        return JsonResponse({'status':True,'message':"Status Changed successfully"})
    except Exception as e:
        return JsonResponse({'status':False,'error':f"unexpected error occured {str(e)}"},status=400)

def create_banner_ads(request):
    try:
        if request.method=='GET':
            users=Account.objects.all().values('email','id')

            homepage_banner_instance=DefaultBannerAdsPricing.objects.filter(position='homepage_carousel').first()
            category_page_top=DefaultBannerAdsPricing.objects.filter(position='category_page_top').first()
            homepage_top_instance=DefaultBannerAdsPricing.objects.filter(position='homepage_top').first()
            homepage_bottom_instance=DefaultBannerAdsPricing.objects.filter(position='homepage_bottom').first()
            categories = Category.objects.filter(parent_id__isnull=True)
        
        # Create a dictionary to hold the categories and their subcategories
            category_context = {}
            for category in categories:
            # Get subcategories for each parent category
                subcategories = Category.objects.filter(parent_id=category)
                category_context[category] = subcategories

            print(homepage_banner_instance.price_per_day)
            context={
                'homepage_banner_instance':homepage_banner_instance,
                'category_page_top':category_page_top,
                'homepage_bottom_instance':homepage_bottom_instance,
                'homepage_top_instance':homepage_top_instance,
                'categories':category_context,
                'users':users
            }
            print(context)
            return render(request,'admin1/banner_ads/add_banner_ads.html',context)
        else:
            data = request.POST
            print(data)
            title = data.get('name')

            link = data.get('link')
            category_id = data.get('category', None)
            subcategory_id = data.get('subcategory', None)
            city = data.get('city_id', None)
            user_id=data.get('user_id',None)

            # Getting the creator of the ad (e.g., the current logged-in user)
            if user_id:
                created_by =Account.objects.get(id=user_id)

            # Extracting the individual banner plans and their respective images
            homepage_plan = data.get('homepage_plan', None)
            homepage_image = request.FILES.get('homepage_image', None)

            category_plan = data.get('category_plan', None)
            category_image = request.FILES.get('category_image', None)

            hometopbanner_plan = data.get('hometopbanner_plan', None)
            hometopbanner_image = request.FILES.get('hometopbanner_image', None)

            homebottombanner_plan = data.get('homebottombanner_plan', None)
            homebottombanner_image = request.FILES.get('homebottombanner_image', None)

            # Category and subcategory objects
            category = Category.objects.get(id=category_id) if category_id else None
            subcategory = Category.objects.get(id=subcategory_id) if subcategory_id else None

            # Function to create a banner ad
            def create_banner_ad(position, plan, image, title, link, category, subcategory, city, created_by):
                if plan:
                    try:
                        print(position)
                        pricing = DefaultBannerAdsPricing.objects.get(position=position)
                        price_per_day = pricing.price_per_day

                        # Calculate the number of days using price/price_per_day
                        days = float(plan) / float(price_per_day)
                        print(float(plan))
                        print(float(price_per_day))

                    except DefaultBannerAdsPricing.DoesNotExist:
                        # Handle the case where no pricing exists for the position
                        return None
                    print(image)
                    banner_ad = BannerAds.objects.create(
                        title=title,
                        link=link,
                        price=float(plan),
                        position=position,
                        city=city,
                        image=image,
                        category=category,
                        days=days,
                        sub_category=subcategory,
                        created_by=created_by,
                        status="pending"  # Default status is pending
                    )
                    return banner_ad

            # Create the banner ad for each plan if it exists
            if homepage_plan:
                create_banner_ad('homepage_carousel', homepage_plan, homepage_image, title, link, category, subcategory, city, created_by)

            if category_plan:
                create_banner_ad('category_page_top', category_plan, category_image, title, link, category, subcategory, city, created_by)

            if hometopbanner_plan:
                create_banner_ad('homepage_top', hometopbanner_plan, hometopbanner_image, title, link, category, subcategory, city, created_by)

            if homebottombanner_plan:
                create_banner_ad('homepage_bottom', homebottombanner_plan, homebottombanner_image, title, link, category, subcategory, city, created_by)

            context={'message':"Banner Ads Submitted Successfully"}
            return redirect(reverse("create_banner_ads"))
     
    except Exception as e:
        print(e)
        return e
def delete_banner_ad(request):
    try:
        banner_id=request.GET.get('banner_id')
        banner_instance=BannerAds.objects.get(id=banner_id)
        banner_instance.delete()
        return JsonResponse({'status':True,'message':"Banner ad deleted succesfully"},status=200)
    except Exception as e:
        return JsonResponse({"status":False,'message':f"Unexpeced error occured {str(e)}"},status=400)



