from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from apps.category.models import Category,SubCategory
from apps.store.models import Product,Feature

# Create your views here.
# def category_view(request):
#     categories = Category.objects.prefetch_related('sub_categories').all()

#     context = {
#         'categories': categories,
#     }

#     print(context)


#     return render(request, 'home/index.html', context)


def listing_view(request, subcategory_slug):
    sub_category = SubCategory.objects.get(slug=subcategory_slug)
    
    sort_by = request.GET.get("sort", "default")
    products = Product.objects.filter(sub_category=sub_category).order_by("-id")
    

    # For pagination
    paginator = Paginator(products, 1)  # Adjust the number for items per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Apply sorting to the items on the current page only
    if sort_by == "low-high":
        page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price)
    elif sort_by == 'high-low':
        page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price, reverse=True)
        
    
    feature=Feature.objects.all()    

    context = {
        'products': page_obj,
        'count': paginator.count,
        'products':products,
        'page_obj': page_obj,
        'current_page_product_count': len(page_obj.object_list),
        'features':feature
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

    return render(request, "listing/listing-sidebar.html", context)


def filter_category(request):
    try:
        query = request.GET.get("query", "")
        category = request.GET.get("category",None)
        location = request.GET.get("location", "")
        region = request.GET.get("region", "")
        min_price = request.GET.get("min_price", None)
        max_price = request.GET.get("max_price", None)

        products = Product.objects.filter(category=category).order_by('-id')

        if query!="":
            products = products.filter(product_name__icontains=query)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        paginator = Paginator(products, 1)  # Show 10 products per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Prepare data for rendering
        
        product_list_html = render_to_string("partials/side_product_list.html", {"products": page_obj}, request=request)
        pagination_context={
            'page_obj':page_obj,
            'category':category,
            'query':query,
            'min_price':min_price,
            'max_price':max_price
        }
        pagination_html = render_to_string("partials/filter_paginations.html", pagination_context, request=request)

        if request.headers.get("x-requested-with") == "FETCH":
            response_data = {
                "product_data": product_list_html,
                "pagination_data": pagination_html,
            }
            return JsonResponse(response_data)
        # Prepare data to be sent as JSON
    except Exception as e:
        print(e)
        #later redirect to 404


def category(request):
    try:
        category = Category.objects.all()
        context = {"category": category}
        return render(request, "others/categories.html", context)

    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponse(
            "An error occurred while processing your request.", status=500
        )




def sub_category_list(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug)
    
        subcategories = SubCategory.objects.filter(parent=category)
     
        
        

        context = {
            "category": category,
            "subcategories": subcategories,
        }
        return render(request, "others/sub_categories.html", context)

    except Exception as e:
        print(f"Error occurred: {e}")
        return HttpResponse(
            "An error occurred while processing your request.", status=500
        )
