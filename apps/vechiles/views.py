from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from apps.category.models import Category
from apps.store.models import BookMark, Feature, Product

#Property landing page
def landing_page(request):
    try:
        category=Category.objects.get(slug='vechiles')
        sub_category_instance=Category.objects.filter(parent_id=category)
        featured_products=Product.objects.filter(category=category)[:4]
        context={
            'subcategories':sub_category_instance,
            'featured_products':featured_products,
            'sub_category_instance':sub_category_instance
        }
        print(context)
        return render(request,'vechiles/landing.html',context)
    except Exception as e:
        print(e)
        # will later return to some 400 page
        return e

def vechiles_category(request):
    try:
        location=request.POST.get('location')
        make=request.POST.get('make')
        model=request.POST.get('models')
        prices_status=request.POST.get('price_status')
        prices_value=request.POST.get('price')
        #used or new
        condition=request.GET.get('condition')


        category = Category.objects.get(slug='vechiles')
        if category is None:
            category=Category.objects.get(slug='vechile')
        products = Product.objects.filter(category=category).order_by("-id")
        if location:
            products = products.filter(location__address__icontains=location)

        print(products)

        if request.user.is_authenticated:
            bookmarked_product_ids = BookMark.objects.filter(
                user=request.user
            ).values_list("product_id", flat=True)
        else:
            bookmarked_product_ids = []
        paginator = Paginator(products, 10)  # Adjust the number for items per page
        page_number = request.GET.get("page",1)
        page_obj = paginator.get_page(page_number)
        feature=Feature.objects.all() 
        print(bookmarked_product_ids,'ids')   

        context = {
            'products': page_obj,
            'count': paginator.count,
            'page_obj': page_obj,
            'category':category,
            'current_page_product_count': len(page_obj.object_list),
            'features':feature,
            'book_mark':bookmarked_product_ids
        }

        if request.headers.get("x-requested-with") == "FETCH":
            product_list = render_to_string(
                "partials/side_product_list.html", context, request=request
            )  # Return only the product list for AJAX
            pagination_data = render_to_string(
                "partials/pagination.html", context, request=request
            )
            response_data = {
                "product_data": product_list,
                "pagination_data": pagination_data,
            }
            return JsonResponse(response_data)

        return render(request, "listing/listing-category.html", context)

    except Exception as e:
        print(e)
        return e
