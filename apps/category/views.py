from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from apps.category.models import Category, Field,SubCategory, SubCategoryInfo
from apps.store.models import Product,Feature,BookMark
from django.db.models import Count


from django.views.decorators.csrf import csrf_exempt

# For subcategory
def listing_view(request, subcategory_slug):
    try:
        print(subcategory_slug)
        sub_category = SubCategory.objects.get(slug=subcategory_slug)
        products = Product.objects.filter(sub_category=sub_category).order_by("-id")
        # For pagination
        paginator = Paginator(products, 10)  # Adjust the number for items per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Apply sorting to the items on the current page only
                
        feature=Feature.objects.all()    

        context = {
            'products': page_obj,
            'count': paginator.count,
            'sub_category':sub_category,
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

        return render(request, "listing/listing-subcategory.html", context)
    except Exception as e:
        print(e)


#For vieweign directly in category
def viewall_listing_view(request, subcategory_slug):
    try:
        category = Category.objects.get(slug=subcategory_slug)
        products = Product.objects.filter(category=category).order_by("-id")
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


def filter_category(request):
    try:
        query = request.GET.get("query", "")
        category = request.GET.get("category",None)
        location = request.GET.get("location", "")
        region = request.GET.get("region", "")
        min_price = request.GET.get("min_price", None)

        sort_by = request.GET.get("sort", "default")
        max_price = request.GET.get("max_price", None)

        products = Product.objects.filter(category=category).order_by('-id')

        if query!="":
            products = products.filter(product_name__icontains=query)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        paginator = Paginator(products, 10)  # Show 10 products per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        if sort_by == "low-high":
            page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price)
        elif sort_by == 'high-low':
            page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price, reverse=True)
        

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

def filter_sub_category(request):
    try:
        print(request.GET)

        sort_by = request.GET.get("sort", "default")
        query = request.GET.get("query", "")
        category = request.GET.get("category",None)
        location = request.GET.get("location", "")
        region = request.GET.get("region", "")
        min_price = request.GET.get("min_price", None)
        max_price = request.GET.get("max_price", None)

        products = Product.objects.filter(sub_category=category).order_by('-id')

        if query!="":
            products = products.filter(product_name__icontains=query)
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        paginator = Paginator(products, 10)  # Show 10 products per page
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Prepare data for rendering
        if sort_by == "low-high":
            page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price)
        elif sort_by == 'high-low':
            page_obj.object_list = sorted(page_obj.object_list, key=lambda x: x.price, reverse=True)
       
        product_list_html = render_to_string("partials/side_product_list.html", {"products": page_obj}, request=request)
        pagination_context={
            'page_obj':page_obj,
            'category':category,
            'query':query,
            'min_price':min_price,
            'max_price':max_price
        }
        pagination_html = render_to_string("partials/filter_subcategory_pagination.html", pagination_context, request=request)

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
        print('sub cateagory list')
        category = get_object_or_404(Category, slug=slug)
        subcategories = SubCategory.objects.filter(parent=category).annotate(product_count=Count('products'))
        print(subcategories,'sub')     
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

def create_category(request):
    try:
        if request.method=="POST":
            print(request.POST)
            data=request.POST
            category_name=data.get('category_name')
            menu_text=data.get('menu_text')
            order=data.get('order')
            type=data.get('type')
            menu_item=data.get('menu_item') in ('yes')
            popular_item=data.get('popular_item') in ('yes')
            featured_item=data.get('featured_item') in ('yes')
            latest_item=data.get('latest_item') in ('yes')
            industry_category=data.get('industry_category') in ('yes')
            media_type=data.get('media_type')
            long_description=data.get('long_description')
            short_description=data.get('short_description')
            status=data.get('status')
            meta_title_country=data.get('meta_title_country')
            meta_description_country=data.get('meta_description_country')
            meta_keywords_country=data.get('meta_keywords_country')
            meta_title_city=data.get('meta_title_city')
            meta_description_city=data.get('meta_description_city')
            meta_keywords_city=data.get('meta_keywords_city')
            
            category_icon_image=request.FILES.get('icon_image')
            category_thumbnail_image=request.FILES.get('thumbnail_image')
            print(category_icon_image,category_thumbnail_image)

            # For subcategory
            parent_category_slug=data.get('category_slug',None)
            print(parent_category_slug)

            
            category_instance=Category.objects.create(category_name=category_name,menu_text=menu_text,order=order,
                                category_type=type,menu_item=menu_item,popular_item=popular_item,featured_item=featured_item,latest_item=latest_item,
                                industry_standard=industry_category,media_type=media_type,long_description=long_description,short_description=short_description,
                                status=status,meta_title_country=meta_title_country,meta_description_country=meta_description_country,meta_keywords_country=meta_keywords_country,meta_title_city=meta_title_city,meta_description_city=meta_description_city,meta_keywords_city=meta_keywords_city,
                                category_icon_image=category_icon_image,category_thumbnail_image=category_thumbnail_image)

            if parent_category_slug is not None:
                parent_category=Category.objects.filter(slug=parent_category_slug).first()
                category_instance.parent_id=parent_category
                category_instance.save()

            print(category_instance)
            context={
                'message':'Category added Success'
            }
            print('tryu')
            return redirect(reverse("add_admin_category"))
        else:
            raise Exception("ONly post method is supported for this endpoitn")
    except Exception as e:
        print(e)
        return (str(e))

def create_field(request):
    try:
        if request.method=='POST':
            data=request.POST
            print(data)
            field_name=data.get('field_name')
            field_type=data.get('field_type')
            mandatory=data.get('mandatory') in ('yes')
            searchable=data.get('searchable') in ('yes')
            featured_style=data.get('featured_style')
            hint=data.get('hint')
            admin_hint=data.get('admin_hint')
            icon=request.FILES.get('field_icon')

            category_instance=Category.objects.filter(category_name=hint).first()
            if category_instance is None:
                raise Exception("The provided hint doesnot have a respective category")
            field_instance=Field.objects.create(field_name=field_name,field_type=field_type,mandatory=mandatory,searchable=searchable,
                                                featured_style=featured_style,hint=hint,admin_hint=admin_hint,icon=icon,linked_to=category_instance)

            return redirect(reverse('admin_fields'))
        else:
            raise Exception("Only post method supported for this endpoint")
    except Exception as e:
        print(e)
        return JsonResponse({'error':str(e)},status=400)

# Will probably changed in configuration
@csrf_exempt
def create_category_info(request):
    try:
        if request.method=="POST":
            print(request.POST)
            data=request.POST
            print(data)
            content_titles=data.getlist('content_title')
            content_types=data.getlist('content_type')
            category=data.get('category')
            content_datas=data.getlist('content_data')
            for i in range(0,len(content_titles)):
                print(content_titles[i],"is of input type",content_types[i] ,'of data',content_datas[i])
            print(content_titles,content_types,category)
            subcategory_instance=SubCategory.objects.filter(id=category).first()
            if subcategory_instance is None:
                raise Exception("Subcategory of that id not found")
            SubCategoryInfo.objects.create(category=subcategory_instance,content_datas=content_datas,content_titles=content_titles,content_types=content_types)
        else:
            raise Exception("Only post method is allowed for this endpoint")
    except Exception as e:
        print(e)
        # will later redirect to error pages 
        return JsonResponse({'error':str(e)},status=400)
