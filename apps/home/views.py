from django.shortcuts import render

from apps.category.models import Category
from apps.store.models import Product

# Create your views here. i am your home


def home(request):
    if request.method=='GET':
        try:
            all_categories = Category.objects.select_related().all().order_by('-id')
            latest_products = []

            # Get the latest 5 products for each category
            for category in all_categories:
                products = Product.objects.select_related().filter(category=category, is_available=True).order_by('-created_date')[:5]
                latest_product = {'products':products,'category':category}
                latest_products.append(latest_product)
            context = {
                'latest_products': latest_products,
                'categories':all_categories
            }
            print(context)
            return render(request,'home/index.html',context)
        except Exception as e:
            print(e)
            #later redirect to some 404 page with custom error message
            return  "error"
    
    
def service_details(request):
    return render(request,'home/service-details.html')    
