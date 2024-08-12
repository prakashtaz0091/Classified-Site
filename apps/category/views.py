from django.shortcuts import render
from apps.category.models import Category
from apps.store.models import Product
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
    context={
        'products':products
    }
    return render(request,'listing/listing-sidebar.html',context)