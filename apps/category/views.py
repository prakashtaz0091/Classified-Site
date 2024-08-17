from django.shortcuts import render
from apps.category.models import Category
from apps.store.models import Product,Feature
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


def listing_view(request, slug):
    category = Category.objects.get(slug=slug)
    sort_by = request.GET.get('sort', 'default')
    products = Product.objects.filter(category=category).order_by('created_date')
    
    
    if request.method=="POST":
        query = request.POST.get('query')
        location = request.POST.get('location')
        region = request.POST.get('region')
        features = request.POST.getlist('features')
        radius = request.POST.get('radius')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')
        
        
        
        if query:
                products = products.filter(product_name__icontains=query)
        if location:
            products = products.filter(location__icontains=location)
        if region:
            products = products.filter(region=region)
        if features:
            products = products.filter(feature__name__in=features).distinct()
        if radius:
            # Add radius filtering logic here
            pass
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
            
        
        paginator = Paginator(products, 3)  # Adjust the number for items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Apply sorting to the items on the current page only
        if sort_by == 'low-high':
            page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price)
        elif sort_by == 'high-low':
            page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price, reverse=True)
            
        
        feature=Feature.objects.all()    

        context = {
            'products': page_obj,
            'count': paginator.count,
            'category': category,
            'page_obj': page_obj,
            'current_page_product_count': len(page_obj.object_list),
            'features':feature
        }

    
        return render(request, 'partials/side_product_list.html', context)
    



    # For pagination
    paginator = Paginator(products, 3)  # Adjust the number for items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Apply sorting to the items on the current page only
    if sort_by == 'low-high':
        page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price)
    elif sort_by == 'high-low':
        page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price, reverse=True)
        
    
    feature=Feature.objects.all()    

    context = {
        'products': page_obj,
        'count': paginator.count,
        'category': category,
        'page_obj': page_obj,
        'current_page_product_count': len(page_obj.object_list),
        'features':feature
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/side_product_list.html', context)  # Return only the product list for AJAX

    return render(request, 'listing/listing-sidebar.html', context)



def search_products(request):
    if request.method == "POST":
        query = request.POST.get('query')
        location = request.POST.get('location')
        region = request.POST.get('region')
        features = request.POST.getlist('features')
        radius = request.POST.get('radius')
        min_price = request.POST.get('min_price')
        max_price = request.POST.get('max_price')

        products = Product.objects.all()

        # Add filtering logic here based on the form data
        if query:
            products = products.filter(product_name__icontains=query)
        if location:
            products = products.filter(location__icontains=location)
        if region:
            products = products.filter(region=region)
        if features:
            products = products.filter(feature__name__in=features).distinct()
        if radius:
            # Add radius filtering logic here
            pass
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        return render(request, 'partials/side_product_list.html', {'products': products})
    return HttpResponse(status=400)




def category(request):
    try:
        category = Category.objects.all()
        print(category, 'category')
        context = {
            'category': category
        }
        return render(request, 'others/categories.html', context)
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponse("An error occurred while processing your request.", status=500)
