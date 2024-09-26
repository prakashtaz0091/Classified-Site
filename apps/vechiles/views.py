from django.shortcuts import render

from apps.store.models import Product

#Property landing page
def landing_page(request):
    try:
        featured_products=Product.objects.all()[:4]
        context={
            'featured_products':featured_products
        }
        print(context)
        return render(request,'vechiles/landing.html',context)
    except Exception as e:
        print(e)
        # will later return to some 400 page
        return e
