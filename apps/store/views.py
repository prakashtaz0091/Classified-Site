from django.shortcuts import render

from apps.store.models import Product

# Create your views here.
    
    
def service_details(request,product_slug):
    try:
        product_instance=Product.objects.filter(slug=product_slug).first()
        if product_instance is None:
            raise Exception("Product with the provided slug is not found")
        return render(request,'home/service-details.html')    
    except Exception as e:
        print(e)
        # will later redirect to 404 pages
        return str(e)
        
