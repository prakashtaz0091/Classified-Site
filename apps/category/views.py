from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from apps.category.models import Category, Field, FieldExtra, FieldExtraContent, FieldOptions
from apps.store.models import BannerAds, Product,Feature,BookMark
from django.db.models import Count
import json
 
from django.views.decorators.csrf import csrf_exempt

# For subcategory
def listing_view(request, subcategory_slug):
    try:
        sub_category = Category.objects.get(slug=subcategory_slug)

        category_banner=BannerAds.objects.filter(sub_category=sub_category).order_by('-id').first()
        print('cateogyr banner',category_banner)
        products = Product.objects.filter(subcategory=sub_category).order_by("-id")
        # For pagination
        paginator = Paginator(products, 10)  # Adjust the number for items per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        bookmarked_product_ids=[]
        if request.user.is_authenticated:
                bookmarked_product_ids = BookMark.objects.filter(
                    user=request.user
                ).values_list("product_id", flat=True)
        else:
                bookmarked_product_ids = []

        fields = Field.objects.filter(field_type__in=['select', 'select_multiple'],linked_to=sub_category)

        # Collecting the field options for each field
        field_data = []
        for field in fields:
            options = FieldOptions.objects.filter(linked_to=field)
            field_data.append({
                'id':field.id,
                'field_name': field.field_name,
                'field_type': field.field_type,
                'options': options  # A queryset of FieldOptions objects related to this field

            })
        print(field_data)
                
        feature=Feature.objects.all()    

        context = {
            'products': page_obj.object_list,
            'count': paginator.count,
            'sub_category':sub_category,
            'page_obj': page_obj,
            'current_page_product_count': len(page_obj.object_list),
            'features':feature,
            'field_data':field_data,
            'book_mark':bookmarked_product_ids,
            'category_banner':category_banner,
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

        if location!="":
            products=products.filter(location__address__icontains=location)

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

@csrf_exempt
def filter_sub_category(request):
    try:
        print(request.POST)
        print("hello")

        sort_by = request.GET.get("sort", "default")
        query = request.POST.get("query", "")
        category = request.POST.get("category",None)
        location = request.POST.get("location", "")
        region = request.POST.get("region", "")
        min_price = request.POST.get("min_price", None)
        max_price = request.POST.get("max_price", None)
        fields_filter=request.POST.getlist('fields_filter',None)

        products = Product.objects.filter(subcategory=category).order_by('-id')

        if query!="":
            products = products.filter(product_name__icontains=query)

        if location!="":
            products=products.filter(location__address__icontains=location)

        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)
        print(products,'products till now ')
        if fields_filter:
            filtered_products = []
            criteria = [tuple(f.split(':')) for f in fields_filter if f!=""]
            print(criteria)

            for product in products:
                featured_data = product.featured_data  # Assuming this is a list of strings

                # Check if the product meets all criteria
                all_criteria_met = all(
                    any(f"{field_name}:{field_value}" in item for item in featured_data)
                    for field_name, field_value in criteria
                )

                if all_criteria_met:
                    filtered_products.append(product)
            products=filtered_products

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
        category = Category.objects.filter(parent_id=None).order_by('-id')
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
        subcategories =Category.objects.filter(parent_id=category).annotate(product_count=Count('products'))
        print(subcategories,'sub')     
        context = {
            "category": category,
            "subcategories": subcategories,
            'title':category.category_name
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

            field_instance=Field.objects.create(field_name=field_name,field_type=field_type,mandatory=mandatory,searchable=searchable,
                                                featured_style=featured_style,hint=hint,admin_hint=admin_hint,icon=icon)

            return redirect(reverse('admin_fields'))
        else:
            
            raise Exception("Only post method supported for this endpoint")
    except Exception as e:
        print(e)
        return JsonResponse({'error':str(e)},status=400)

def create_field_options(request,id):
    try:
        if request.method=='POST':
            data=request.POST
            print(data)
            field_id=id
            option_value=data.get('option_value')
            option_order=data.get('option_order')

            field_instance=Field.objects.filter(id=field_id).first()
            if field_instance is None:
                raise Exception("The provided hint doesnot have a respective category")
            field_instance=FieldOptions.objects.create(field_value=option_value,order=option_order,linked_to=field_instance)
            return redirect(reverse('add_options', kwargs={'id': id}))
        else:
          
            raise Exception("Only post method supported for this endpoint")
    except Exception as e:
        print(e)
        return JsonResponse({'error':str(e)},status=400)

def create_field_options_extra(request,id):
    try:
        if request.method=='POST':
            data=request.POST
            print(data,id)
            print('helo world====================+++>')
            field_option_id=id
            menu_text=data.get('menu_text')

            field_options_instance=FieldOptions.objects.filter(id=field_option_id).first()
            if field_options_instance is None:
                raise Exception("The provided hint doesnot have a respective category")
            field_options_extra_instance=FieldExtra.objects.create(menu_text=menu_text,linked_to=field_options_instance)

            return redirect(reverse('extra_information',kwargs={'id': id}))
        else:
            raise Exception("Only post method supported for this endpoint")
    except Exception as e:
        print(e)
        return JsonResponse({'error':str(e)},status=400)


def create_field_options_extra_content(request):
    try:
        if request.method=='POST':
            data=request.POST
            print(data,'==============+++>')
            id=data.get('item_id')
            main_id=data.get('main_id')
            field_extra_id=id
            name=data.get('name')

            field_extra_instance=FieldExtra.objects.filter(id=field_extra_id).first()
            if field_extra_instance is None:
                raise Exception("The provided hint doesnot have a respective category")
            field_options_extra_instance=FieldExtraContent.objects.create(name=name,linked_to=field_extra_instance)

            return JsonResponse({'status': 'success'})
        else:
            raise Exception("Only post method supported for this endpoint")
    except Exception as e:
        print(e)
        return JsonResponse({'error':str(e)},status=400)


from django.http import JsonResponse

def get_category_options(request):
    try:
        category_id = request.GET.get('subcategory_id')
        # Retrieve the category by ID
        category = Category.objects.filter(id=category_id).first()
        
        if not category:
            return JsonResponse({'error': 'Category not found'}, status=404)
        
        # Get all fields related to the category
        print(category.category_name)
        fields = Field.objects.filter(linked_to=category)
        print(fields)
        
        # Prepare the response data
        fields_data = []

        for field in fields:
            # Prepare field data
            field_data = {
                'field_name': field.field_name,
                'field_type': field.field_type,
                'mandatory': field.mandatory,
                'searchable': field.searchable,
                'featured_style': field.featured_style,
                'sub_type': field.sub_type,
                'icon': field.icon.url if field.icon else None
            }
            
            # If the field type is 'select', include the options
            if field.field_type == 'select' or field.field_type=='select_multiple' or field.field_type=='radio':
                options = FieldOptions.objects.filter(linked_to=field).order_by('order')
                field_data['options'] = []
                
                for option in options:
                    option_data = {'value': option.field_value}
                    
                    # Check if there are FieldExtras linked to this option
                    extras = FieldExtra.objects.filter(linked_to=option,disabled=False).order_by('menu_text')
                    if extras.exists():
                        option_data['extras'] = []
                        for extra in extras:
                            extra_data = {
                                'menu_text': extra.menu_text,
                                'mandatory': extra.mandatory,
                                'disabled': extra.disabled
                            }
                            
                            # Include FieldExtraContent if exists
                            contents = FieldExtraContent.objects.filter(linked_to=extra).order_by('order')
                            if contents.exists():
                                extra_data['content'] = [{'name': content.name} for content in contents]
                                option_data['extras'].append(extra_data)
                            
                    
                    field_data['options'].append(option_data)
            
            fields_data.append(field_data)
            print(fields_data)
        
        return JsonResponse({'fields': fields_data}, safe=False)
    
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def toggle_disabled(request):
    extra_id = request.POST.get('id')
    is_disabled = request.POST.get('disabled') == 'true'
    
    try:
        extra = FieldExtra.objects.get(id=extra_id)
        extra.disabled = is_disabled
        extra.save()
        return JsonResponse({'status': 'success', 'disabled': extra.disabled})
    except FieldExtra.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)

