from django.shortcuts import render

from apps.store.models import Product, ProductImages

# Create your views here.
    
    
def service_details(request,product_slug):
    try:
        product_instance=Product.objects.filter(slug=product_slug).first()
        product_instance.view_count+=1
        product_instance.save()
        if product_instance is None:
            raise Exception("Product with the provided slug is not found")
        product_images=ProductImages.objects.filter(product=product_instance)
        context={
            'product':product_instance,
            'product_images':product_images
        }
        return render(request,'home/service-details.html',context)    
    except Exception as e:
        print(e)
        # will later redirect to 404 pages
        return str(e)
        
