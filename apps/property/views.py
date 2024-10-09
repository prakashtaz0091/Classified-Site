from django.shortcuts import render
from apps.category.models import Category
from apps.store.models import Product
from django.core.paginator import Paginator
from django.db.models import Count

#Property landing page
def landing_page(request):
    try:
       
        featured_products = Product.objects.all().order_by('-id')[:4]
        category=Category.objects.get(slug='real-estate')
        all_categories = Category.objects.filter(parent_id=category.id, status='ACTIVE').annotate(product_count=Count('products'))
        latest_products = []
        all_products = (
            Product.objects.select_related()
            .filter(is_available=True, is_approved=True)
            .order_by("-created_date")
        )
        
        # Get the latest 5 products for each category
        for category in all_categories:
            products = all_products.filter(category=category, is_approved=True, is_available=True)[:4]
            latest_product = {"products": products, "category": category}
            latest_products.append(latest_product)

        # Context to pass to the template
        context = {
            'featured_products': featured_products,
            'latest_products': latest_products,
            'subcategories': all_categories,  # This will include the annotated product count
        }
        
        print('hello wrold')

        return render(request, 'properties/landing.html', context)

    except Exception as e:
        # Handle any potential errors here, such as logging them
        print(f"Error in landing_page: {e}")
        return render(request, 'error_page.html')






def listing_list_details(request,slug):
    product=Product.objects.get(slug=slug)
    context={
        'product':product
    }
    return render(request,'properties/list_details.html',context)




def search_property(request):
    all_categories = Category.objects.filter(parent_id=12,status='ACTIVE')  
    all_products = (
            Product.objects.select_related()
            .filter(is_available=True,is_approved=True)
            .order_by("-created_date")
        )  
    latest_products = all_products.filter(category__in=all_categories)
    property_location = request.GET.get('property', '')  
    price = request.GET.get('price', '')  
    category = request.GET.get('category', '') 
    
    print(property_location,price,category)
    
    if property_location:
        latest_products = latest_products.filter(location__address__icontains=property_location)

    if price:
        price = float(price)
        latest_products = latest_products.filter(price__lte=price)


    if category and category != 'all':
        latest_products = latest_products.filter(category__category_name=category)  
        
        
    paginator = Paginator(latest_products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)    
        
        
    context={
        'products':page_obj,
        'page_obj':page_obj
    }    
    return render(request,'properties/search.html',context)








# from django.db.models import Count
# def view_company(request):
#     category = Category.objects.annotate(subcategory_count=Count('subcategories'))
#     context={
#         'category':category
#     }
#     return render(request,'others/categories.html',context)