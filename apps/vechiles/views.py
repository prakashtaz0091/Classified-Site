from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from apps.category.models import Category
from apps.home.models import ProductReview
from apps.store.models import BookMark, Feature, Product

#Property landing page
def landing_page(request):
    try:
        category=Category.objects.get(slug='vechiles')
        sub_category_instance=Category.objects.filter(parent_id=category)
        featured_products=Product.objects.filter(category=category)[:4]

        for product in featured_products:
                    avg_rating=ProductReview.average_rating_for_product(product.id)
                    product.avg_rating=avg_rating

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
        print(request.POST)
        location=request.POST.get('location')
        make=request.POST.get('make')
        model=request.POST.get('models')
        prices_value=request.POST.get('price')
        #used or new
        condition=request.POST.get('condition')
        registered=request.POST.get('status')

        make_query=request.GET.get('make')
        model_query=request.GET.get('model')
        condition_query=request.GET.get('condition')
        price_query=request.GET.get('price')
        mileage_query=request.GET.get('mileage')

        if make:
            make_query=make
        if model:
            model_query=model
        if prices_value:
            price_query=prices_value
        if condition:
            condition_query=condition

        category = Category.objects.get(slug='cars')
        if category is None:
            category=Category.objects.get(slug='cars')

        products = Product.objects.filter(subcategory=category).order_by("-id")
        if location:
            products = products.filter(location__address__icontains=location)

        query = request.GET.get("query", "")
        category = request.GET.get("category",None)
        location_query = request.GET.get("location", "")
        region = request.GET.get("region", "")
        min_price = request.GET.get("min_price", None)

        sort_by = request.GET.get("sort", "default")
        max_price = request.GET.get("max_price", None)

        if location:
            location_query=location

        if query!="":
            products = products.filter(product_name__icontains=query)

        if location_query!="":
            products=products.filter(location__address__icontains=location)

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        if price_query:
            products=products.filter(price__gte=price_query)

        #Accessing data from fields
        if make_query:
            filtered_products=[]
            for product in products:
                featured_data=product.featured_data
                if (make_query.lower() in str(featured_data).lower()):
                    filtered_products.append(product)
            products=filtered_products

        #Accessing data from fields
        if registered:
            filtered_products=[]
            for product in products:
                featured_data=product.featured_data
                if (f'status:{registered.lower()}' in str(featured_data).lower()):
                    filtered_products.append(product)
            products=filtered_products


        if condition_query:
            filtered_products=[]
            for product in products:
                featured_data=product.featured_data
                if (condition_query.lower() in str(featured_data).lower()):
                    filtered_products.append(product)
            products=filtered_products

       
        if model_query:
            filtered_products=[]
            for product in products:
                featured_data=product.featured_data
                if (model_query.lower() in str(featured_data).lower()):
                    filtered_products.append(product)
            products=filtered_products
       
        if mileage_query:
            filtered_products=[]
            for product in products:
                featured_data=product.featured_data
                if (mileage_query.lower() in str(featured_data).lower()):
                    filtered_products.append(product)
            products=filtered_products



        if request.user.is_authenticated:
            bookmarked_product_ids = BookMark.objects.filter(
                user=request.user
            ).values_list("product_id", flat=True)
        else:
            bookmarked_product_ids = []

        paginator = Paginator(products, 10)  # Adjust the number for items per page
        page_number = request.GET.get("page",1)
        page_obj = paginator.get_page(page_number)
        if sort_by == "low-high":
            page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price)
        elif sort_by == 'high-low':
            page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price, reverse=True)
        


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
