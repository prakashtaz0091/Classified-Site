import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import redirect, render

from django.db.models import Sum
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from apps.accounts.models import Account
from apps.category.models import Category
from apps.home.models import Reviews
from apps.store.models import (BannerAds, BookMark, ContactInformation, DefaultBannerAdsPricing, Feature, Location,
                               Product, ProductImages)

from django.db.models import F, Value
from django.db.models.functions import Substr


def home(request):
    if request.method == "GET":
        try:
            # Fetch all categories
<<<<<<< HEAD
            all_categories = Category.objects.select_related().filter(parent_id=None,status='ACTIVE').order_by("-id")
=======
            all_categories = Category.objects.select_related().filter(parent_id=None, status='ACTIVE').order_by("-id")
>>>>>>> origin/master
            latest_products = []
            all_products = (
                Product.objects.select_related()
                .filter(is_available=True)
                .order_by("-created_date")
            )
            
<<<<<<< HEAD
         
=======
          
>>>>>>> origin/master
            # Get the latest 5 products for each category
            for category in all_categories:

                products = all_products.filter(category=category)[:5]

                latest_product = {"products": products, "category": category}
                latest_products.append(latest_product)

            # Fetch bookmarked product IDs if the user is authenticated
            if request.user.is_authenticated:
                bookmarked_product_ids = BookMark.objects.filter(
                    user=request.user
                ).values_list("product_id", flat=True)
            else:
                bookmarked_product_ids = []
            
            
            print(latest_products,'latest one')    
            print(all_products  ,  'all products')    

            context = {
                "latest_products": latest_products,
                "all_products": all_products,
                "categories": all_categories,
                "book_mark": bookmarked_product_ids,
            }

            return render(request, "home/index.html", context)
        except Exception as e:
            print("Error:")
            print(e)
            # Redirect to a custom error page or return an error response
            return render(request, "home/error.html", {"error": str(e)})


def privacy(request):
    # return render(request,'company/')
    pass


def freq_question(requset):
    return render(requset, "company/faq.html")


def terms(request):
    return render(request, "company/terms-condition.html")


# def contact(request):
#     return render(request, "company/contact.html")


def how_it_works(request):
    return render(request, "company/howitworks.html")



def dashboard(request):
    try:
<<<<<<< HEAD
        book_marks=BookMark.objects.filter(user=request.user)
        total_product=Product.objects.filter(created_by=request.user,is_available=True,is_approved=True).count()
        reviews_list=Reviews.objects.select_related().filter(reviewed_for=request.user).order_by('-id')[:5]
        reviews_count=Reviews.objects.filter(reviewed_for=request.user).count()
        total_views = Product.objects.filter(created_by=request.user,is_available=True,is_approved=True).aggregate(total_views=Sum('view_count'))['total_views']
        
       
=======
        user=request.GET.get('user',None)
        user_id=request.GET.get('id',None)

        user_to_view=None
        if user is None:
            user_to_view=request.user
        else:
            user_instance=Account.objects.filter(id=user_id).first()
            user_to_view=user_instance
            user_to_view.prefix_email=user

        book_marks=BookMark.objects.filter(user=user_to_view)
        total_product=Product.objects.filter(created_by=user_to_view).count()
        reviews_list=Reviews.objects.select_related().filter(reviewed_for=user_to_view).order_by('-id')[:5]
        reviews_count=Reviews.objects.filter(reviewed_for=user_to_view).count()
        total_views = Product.objects.filter(created_by=user_to_view).aggregate(total_views=Sum('view_count'))['total_views']
>>>>>>> origin/master
        bookmarks_count=book_marks.count()

        if user:
            context={
                'book_marks':book_marks,
                'bookmarks_count':bookmarks_count,
                'reviews_list':reviews_list,
                'total_product':total_product,
                'reviews_count':reviews_count,
                'total_views':total_views,
                'type':'viewing',
                'user_to_view':user_to_view,
            }
        else:
            context={
                'book_marks':book_marks,
                'bookmarks_count':bookmarks_count,
                'reviews_list':reviews_list,
                'total_product':total_product,
                'reviews_count':reviews_count,
                'total_views':total_views
            }

        return render(request, "others/dashboard.html", context)
    except Exception as e:
        print(e)
        # will later redirect to 404 page


def my_listing(request):
    if request.method == "GET":

        user=request.GET.get('user',None)
        user_id=request.GET.get('id',None)

        user_to_view=None
        if user is None:
            user_to_view=request.user
        else:
            user_instance=Account.objects.filter(id=user_id).first()
            user_to_view=user_instance
            user_to_view.prefix_email=user


        sort_option = request.GET.get("sort", "-created_date")  # Default to newest
        search_query = request.GET.get("search", "")  # Default to newest
        products=None
        if search!="":
            products = Product.objects.filter(
            product_name__icontains=search_query,is_available=True,is_approved=True
        ) | Product.objects.filter(
            description__icontains=search_query,is_available=True,is_approved=True
        )
<<<<<<< HEAD
            products = products.filter(created_by=request.user,is_available=True,is_approved=True).order_by(sort_option)
        else:
            products = Product.objects.filter(created_by=request.user,is_available=True,is_approved=True).order_by(sort_option)
=======
            products = products.filter(created_by=user_to_view).order_by(sort_option)
        else:
            products = Product.objects.filter(created_by=user_to_view).order_by(sort_option)

        if user is not None:
            products=products.filter(is_approved=True)
>>>>>>> origin/master
        paginator = Paginator(products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if request.headers.get("x-requested-with") == "FETCH" or request.headers.get('x-requested-with')=="XMLHttpRequest":
            product_data = render_to_string(
                    "partials/product_list_mylist.html",
                    {"products": page_obj.object_list},
                    request=request,
                ),
            pagination_context={
                'page_obj':page_obj,
                'search':search_query,
                'sort':sort_option

            }
            pagination_data=render_to_string(
                "partials/pagination_mylist.html",
                pagination_context,
                request=request
            )
            return JsonResponse({'product_data':product_data,'pagination_data':pagination_data})

        context = {
            "page_obj": page_obj,
            "products": page_obj.object_list,
        }
        if  user is not None:
            context['type']='viewing'
            context['user_to_view']=user_to_view

        return render(request, "others/my-listing.html", context)


def edit_my_listing(request, id):
    product = Product.objects.get(id=id)
    if request.method == "GET":

        features = Feature.objects.all()
        categories = Category.objects.filter(status='ACTIVE')
        product_images = ProductImages.objects.filter(product=product)
        selected_category=[]
        selected_categories = selected_category.append(product.category.id)
        selected_features = product.features.all().values_list("id", flat=True)

        context = {
            "product": product,
            "categories": categories,
            "product_images": product_images,
            "selected_categories": selected_category,
            "selected_features": selected_features,
            "features": features,
            "id": id,
        }

        return render(request, "others/edit_my_listing.html", context)
    else:
        # Update basic product details

        product.product_name = request.POST.get("product_name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.tagline = request.POST.get("tagline")
        product.is_available = True

        # Update location details
        product.location.Location = request.POST.get("location")
        product.location.address = request.POST.get("address")
        product.location.map_address = request.POST.get("map_address")
        product.location.latitude = request.POST.get("latitude")
        product.location.longitude = request.POST.get("longitude")
        product.location.save()

        # Update contact information
        product.contact_information.email = request.POST.get("email")
        product.contact_information.website = request.POST.get("website")
        product.contact_information.phone = request.POST.get("phone")
        product.contact_information.save()

        # Update categories
        selected_categories = request.POST.getlist("categories")
        product.category.set(selected_categories)

        # Update features
        selected_features = request.POST.getlist("features")
        product.features.set(selected_features)

        # Handle cover image update
        cover_image = request.FILES.get("cover_image")
        if cover_image:
            product.cover_image = cover_image

        # Handle gallery images update
        gallery_images = request.FILES.getlist("gallery_images")
        if gallery_images:
            ProductImages.objects.filter(product=product).delete()
            for image in gallery_images:
                ProductImages.objects.create(product=product, image=image)

        # Save all changes to the product
        product.save()

        print("saved")

        return redirect("my_listing")  # Redirect to an appropriate page after saving


def delete_my_listing(request, id):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect("my_listing")

    except:
        return redirect("error")


def something_wrong(request):
    return render(request, "error/error-500.html")


def book_marks(request):

    try:
        user=request.GET.get('user',None)
        user_id=request.GET.get('id',None)

        user_to_view=None
        if user is None:
            user_to_view=request.user
        else:
            user_instance=Account.objects.filter(id=user_id).first()
            user_to_view=user_instance
            user_to_view.prefix_email=user


        book_marks = BookMark.objects.filter(user=user_to_view).order_by('-id')
        if request.user.is_authenticated:
            bookmarked_product_ids = BookMark.objects.filter(
                user=user_to_view
            ).values_list("product_id", flat=True)
        else:
            bookmarked_product_ids = []
            
            
        print(bookmarked_product_ids,'id')    

        # paginations added
        paginator = Paginator(book_marks, 1)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if request.headers.get("x-requested-with") == "FETCH" or request.headers.get('x-requested-with')=="XMLHttpRequest":
                product_data = render_to_string(
                        "partials/product_list_bookmark.html",
                        {"book_marks": page_obj.object_list},
                        request=request,
                    ),
                pagination_data=render_to_string(
                    "partials/pagination.html",
                    {'page_obj':page_obj},
                    request=request
                )
                print(pagination_data)
                return JsonResponse({'product_data':product_data,'pagination_data':pagination_data})
        context = {"book_marks": page_obj, "page_obj": page_obj, "count": paginator.count,'book_mark':bookmarked_product_ids}
        if user_id:
            context['type']='viewing'
            context['user_to_view']=user_to_view

        return render(request, "others/bookmarks.html", context)

    except Exception as e:
        print(e)
        # will do more things like 404 page later

def messages(request):
    return render(request, "others/messages.html")


def reviews(request):
    try:
        user=request.GET.get('user',None)
        user_id=request.GET.get('id',None)

        user_to_view=None
        if user is None:
            user_to_view=request.user
        else:
            user_instance=Account.objects.filter(id=user_id).first()
            user_to_view=user_instance
            user_to_view.prefix_email=user



        visitor_reviews_list = (
            Reviews.objects.select_related()
            .filter(reviewed_for=user_to_view)
            .order_by("-id")
        )
        your_reviews_list = (
            Reviews.objects.select_related()
            .filter(created_by=user_to_view)
            .order_by("-id")
        )
        context = {
            "visitor_reviews_list": visitor_reviews_list,
            "your_reviews_list": your_reviews_list,
        }
        if user_id:
            context['type']='viewing'
            context['user_to_view']=user_to_view
        return render(request, "others/reviews.html", context)
    except Exception as e:
        print(e)
        # will later forward to 404 page


# For customers to provide feedback or opinions to user
from apps.store.views import decode_id
def feedback(request, hashed_user_id):
    try:
        print(hashed_user_id)
        decoded_id=decode_id(hashed_user_id)
        print(decoded_id)
        review_for=Account.objects.filter(id=decoded_id).values('full_name').first()

        context={
            'review_for':review_for.get('full_name')
        }
        print(context)
            
        return render(request, "home/feedback.html",context)
    except Exception as e:
        print(e)
        # will later move it to 404 page
        return e

    return render(request, "others/reviews.html")


@login_required(login_url="/account/login/")
def add_listing(request):
    if request.method == "POST":
        print(request.POST)
        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        tagline = request.POST.get("tagline")
        selected_categories = request.POST.get("categories")
        selected_sub_categories = request.POST.get("subcategories")
        selected_features = request.POST.getlist("features")
        featured_data_json=request.POST.get('form_data')
        featured_data=json.loads(featured_data_json)
        
        data_file=request.FILES.get('data-file')
        data_file_name=request.POST.get('data-file-name')
        print(data_file)
        # Retrieve location data
        location_name = request.POST.get("location")
        address = request.POST.get("address")
        map_address = request.POST.get("map_address")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        # Retrieve contact information
        email = request.POST.get("email")
        website = request.POST.get("website")
        phone = request.POST.get("phone")

        # Save location
        location = Location.objects.create(
            Location=location_name,
            address=address,
            map_address=map_address,
            latitude=latitude,
            longitude=longitude,
        )

        # Save contact information
        contact_information = ContactInformation.objects.create(
            email=email,
            website=website,
            phone=phone,
        )

        # Save product without categories first
        product = Product.objects.create(
            product_name=product_name,
            description=description,
            price=price,
            tagline=tagline,
            location=location,
            contact_information=contact_information,
            is_available=True,
            created_by=request.user,
            featured_data=featured_data,
        )


        # Add selected categories to the product
        category = Category.objects.filter(id=selected_categories,status='ACTIVE').first()
        subcategory = Category.objects.filter(id=selected_sub_categories,status='ACTIVE').first()
        product.category=category
        product.subcategory=subcategory

        for feature_id in selected_features:
            feature = Feature.objects.get(id=feature_id)
            product.features.add(feature)

        # Handle file uploads for cover image
        cover_image = request.FILES.get("cover_image")
        if cover_image:
            product.cover_image = cover_image
            product.save()
            print("Cover image uploaded")

        # Handle file uploads for gallery images
        gallery_images = request.FILES.getlist("gallery_images")
        for image in gallery_images:
            ProductImages.objects.create(product=product, image=image)
        product.save()
        print("Gallery images uploaded")
        return JsonResponse({'status':True,'message':"ad added success"},status=200)

    else:    
        category=Category.objects.filter(parent_id=None,status='ACTIVE')
        features=Feature.objects.all()
        context={
            'categories':category,
            'features':features
        }
        return render(request,'listing/add-listing.html',context)


def get_subcategories(request):
    if request.method == "GET":
        category_id = request.GET.get('category_id')
        subcategories = Category.objects.filter(parent_id=category_id,status='ACTIVE')
        subcategory_list = [
            {
                "id": sub.id,
                "category_name": sub.category_name,
            }
            for sub in subcategories
        ]
        return JsonResponse({"subcategories": subcategory_list})
    
    
    
def all_ads(request):
    product_list=Product.objects.filter(is_available=True,is_approved=True).order_by('-created_date')
    if request.user.is_authenticated:    
        bookmarked_product_ids = BookMark.objects.filter(user=request.user).values_list('product_id', flat=True)
    else: 
        bookmarked_product_ids = []
    
    paginator = Paginator(product_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products = page_obj.object_list  # Get the list of products on the current page

    context = {
        'page_obj': page_obj,
        'products': products,
        'book_mark':bookmarked_product_ids
    }
    return render(request, 'listing/listing-grid.html', context)





def sub_category(request):
   print('hello its sub category')
   return render(request,'others/sub_categories.html')





def search(request):
    category_slug= request.GET.get('category')
    location = request.GET.get('location')
    products = Product.objects.filter(is_available=True,is_approved=True).order_by('-id')

    bookmarked_product_ids=[]
    if request.user.is_authenticated:
                bookmarked_product_ids = BookMark.objects.filter(
                    user=request.user
                ).values_list("product_id", flat=True)
    else:
                bookmarked_product_ids = []

    print(bookmarked_product_ids)
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if location:
        products = products.filter(location__address__icontains=location)
        
    # Pagination logic
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 1)  # Show 10 products per page
    products=None
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    

    if request.headers.get("x-requested-with") == "FETCH" or request.headers.get('x-requested-with')=="XMLHttpRequest":
            product_data = render_to_string(
                    "partials/product_list_search.html",
                    {"products": products.object_list,
                        'book_mark':bookmarked_product_ids
                     },
                    request=request,
                ),
            pagination_data=render_to_string(
                "partials/pagination_search.html",
                {'page_obj':products,
                 'category':category_slug,
                 'location':location,
                 },
                request=request
            )
            print(pagination_data)
            return JsonResponse({'product_data':product_data,'pagination_data':pagination_data})
    context = {
        'products': products,
        'category': category_slug,
        'location': location,
        'book_mark':bookmarked_product_ids
    }

    return render(request, 'others/search.html', context)


def job(request):
    return render(request,'home/index-8.html')




def banner(request):
    return render(request,'home/banner_list.html')

def add_banner(request):
    if request.method=='GET':
        homepage_banner_instance=DefaultBannerAdsPricing.objects.filter(position='homepage_carousel').first()
        category_page_top=DefaultBannerAdsPricing.objects.filter(position='category_page_top').first()
        homepage_top_instance=DefaultBannerAdsPricing.objects.filter(position='homepage_top').first()
        homepage_bottom_instance=DefaultBannerAdsPricing.objects.filter(position='homepage_bottom').first()
        categories = Category.objects.filter(parent_id__isnull=True)
    
    # Create a dictionary to hold the categories and their subcategories
        category_context = {}
        for category in categories:
        # Get subcategories for each parent category
            subcategories = Category.objects.filter(parent_id=category)
            category_context[category] = subcategories

        print(homepage_banner_instance.price_per_day)
        context={
            'homepage_banner_instance':homepage_banner_instance,
            'category_page_top':category_page_top,
            'homepage_bottom_instance':homepage_bottom_instance,
            'homepage_top_instance':homepage_top_instance,
            'categories':category_context
        }
        return render(request,'home/banner.html',context)
    elif  request.method=="POST":
        data = request.POST
        print(data)
        title = data.get('title')

        link = data.get('link')
        category_id = data.get('category', None)
        subcategory_id = data.get('subcategory', None)
        city = data.get('city_id', None)

        # Getting the creator of the ad (e.g., the current logged-in user)
        created_by = request.user if request.user.is_authenticated else None

        # Extracting the individual banner plans and their respective images
        homepage_plan = data.get('homepage_plan', None)
        homepage_image = request.FILES.get('homepage_image', None)

        category_plan = data.get('category_plan', None)
        category_image = request.FILES.get('category_image', None)

        hometopbanner_plan = data.get('hometopbanner_plan', None)
        hometopbanner_image = request.FILES.get('hometopbanner_image', None)

        homebottombanner_plan = data.get('homebottombanner_plan', None)
        homebottombanner_image = request.FILES.get('homebottombanner_image', None)

        # Category and subcategory objects
        category = Category.objects.get(id=category_id) if category_id else None
        subcategory = Category.objects.get(id=subcategory_id) if subcategory_id else None

        # Function to create a banner ad
        def create_banner_ad(position, plan, image, title, link, category, subcategory, city, created_by):
            if plan:
                try:
                    print(position)
                    pricing = DefaultBannerAdsPricing.objects.get(position=position)
                    price_per_day = pricing.price_per_day

                    # Calculate the number of days using price/price_per_day
                    days = float(plan) / float(price_per_day)
                    print(float(plan))
                    print(float(price_per_day))

                except DefaultBannerAdsPricing.DoesNotExist:
                    # Handle the case where no pricing exists for the position
                    return None
                print(image)
                banner_ad = BannerAds.objects.create(
                    title=title,
                    link=link,
                    price=float(plan),
                    position=position,
                    city=city,
                    image=image,
                    category=category,
                    days=days,
                    sub_category=subcategory,
                    created_by=created_by,
                    status="pending"  # Default status is pending
                )
                return banner_ad

        # Create the banner ad for each plan if it exists
        if homepage_plan:
            create_banner_ad('homepage_carousel', homepage_plan, homepage_image, title, link, category, subcategory, city, created_by)

        if category_plan:
            create_banner_ad('category_page_top', category_plan, category_image, title, link, category, subcategory, city, created_by)

        if hometopbanner_plan:
            create_banner_ad('homepage_top', hometopbanner_plan, hometopbanner_image, title, link, category, subcategory, city, created_by)

        if homebottombanner_plan:
            create_banner_ad('homepage_bottom', homebottombanner_plan, homebottombanner_image, title, link, category, subcategory, city, created_by)

        context={'message':"Banner Ads Submitted Successfully"}
        return redirect(reverse('add_banner'))
        return render(request,'home/banner.html',context)


def payment_process(request):
    return render(request,'home/paymentselect.html')

def backup(request):
    return render(request,'home/backup.html')


    
