from django.shortcuts import render
from apps.category.models import Category
from apps.store.models import Product
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# Create your views here.
# def category_view(request):
#     categories = Category.objects.prefetch_related('sub_categories').all()

#     context = {
#         'categories': categories,
#     }
    
#     print(context)
    
    
#     return render(request, 'home/index.html', context)



def listing_view(request,slug):
    category=Category.objects.get(slug=slug)
    products=Product.objects.filter(category=category)
    count=products.count()
    
    
    # for pagination 
    
    
    paginator = Paginator(products, 2)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

    context = {
        'products': page_obj, 
        'count': paginator.count,
        'category': category,  
        'page_obj': page_obj, 
    }
   
    return render(request,'listing/listing-sidebar.html',context)

