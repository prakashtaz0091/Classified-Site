from django.http import JsonResponse
from django.shortcuts import render,redirect

from apps.category.models import Category,Field,FieldOptions,FieldExtra
from apps.store.models import  Product
# Create your views here.


def admin_index(request):
    return render(request,'admin1/index.html')



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

def ads_details(request):
    return render(request,'admin1/Ads/ads_details.html')

