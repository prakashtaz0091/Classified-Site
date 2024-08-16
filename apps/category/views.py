from django.shortcuts import render
from apps.category.models import Category
from apps.store.models import Product
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


# Create your views here.
# def category_view(request):
#     categories = Category.objects.prefetch_related('sub_categories').all()

#     context = {
#         'categories': categories,
#     }
    
#     print(context)
    
    
#     return render(request, 'home/index.html', context)



def listing_view(request,slug):
    try:
        category=Category.objects.get(slug=slug)
        products=Product.objects.filter(category=category)
        count=products.count()
        # for pagination 
        paginator = Paginator(products, 1)  
        page_number = request.GET.get('page')  
        page_obj = paginator.get_page(page_number)  

        context = {
            'products': page_obj, 
            'count': paginator.count,
            'category': category,  
            'page_obj': page_obj, 
            'count':count
        }
        return render(request,'listing/listing-sidebar.html',context)
    except Exception as e:
        print(e)
        # will later redirect to 400 pages





def search(request):
    query = request.GET.get('searchQuery', '')
    category = request.GET.get('categorySelect', '')
    location = request.GET.get('locationInput', '')
    region = request.GET.get('regionSelect', '')
    min_price = request.GET.get('minPrice', None)
    max_price = request.GET.get('maxPrice', None)
 
    products = Product.objects.all()

    if query:
        products = products.filter(product_name__icontains=query) 
    if category:
        products = products.filter(category__icontains=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Prepare data to be sent as JSON
    product_list = list(products.values('id', 'product_name', 'price', 'description', 'cover_image'))
    
    return JsonResponse(product_list, safe=False)




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
