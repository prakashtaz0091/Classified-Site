from django.shortcuts import render
from apps.category.models import Category
from apps.store.models import Product
from django.core.paginator import Paginator


#Property landing page
def landing_page(request):
    try:
        featured_products = Product.objects.all().order_by('-id')[:4]
        all_categories = Category.objects.select_related().filter(parent_id="12",status='ACTIVE')
        property_category = Category.objects.get(category_name='Real Estate')
        subcategories = property_category.subcategories.all()
        
        latest_products = []
        all_products = (
            Product.objects.select_related()
            .filter(is_available=True,is_approved=True)
            .order_by("-created_date")
        )
            # Get the latest 5 products for each category
        for category in all_categories:
            products = all_products.filter(category=category,is_approved=True,is_available=True)[:4]
            latest_product = {"products": products, "category": category}
            latest_products.append(latest_product)
            

        context={
            'featured_products':featured_products,
            'latest_products':latest_products,
            'subcategories':subcategories
        }
        return render(request,'properties/landing.html',context)

    except Exception as e:
        print(e)
        # will later return to some 400 page
        return e








def listing_list_details(request,slug):
    product=Product.objects.get(slug=slug)
    context={
        'product':product
    }
    return render(request,'properties/list_details.html',context)