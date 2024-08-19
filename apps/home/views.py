from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from apps.accounts.models import Account
from apps.category.models import Category
from apps.home.models import Reviews
from apps.store.models import (BookMark, ContactInformation, Feature, Location,
                               Product, ProductImages)


def home(request):
    if request.method == "GET":
        try:
            # Fetch all categories
            all_categories = Category.objects.select_related().all().order_by("-id")
            latest_products = []
            all_products = (
                Product.objects.select_related()
                .filter(is_available=True)
                .order_by("-created_date")
            )
            
            print(all_products,'all products ')

            # Get the latest 5 products for each category
            for category in all_categories:

                products = (
                    Product.objects.select_related()
                    .filter(category=category, is_available=True)
                    .order_by("-created_date")[:5]
                )

                latest_product = {"products": products, "category": category}
                latest_products.append(latest_product)

            # Fetch bookmarked product IDs if the user is authenticated
            if request.user.is_authenticated:
                bookmarked_product_ids = BookMark.objects.filter(
                    user=request.user
                ).values_list("product_id", flat=True)
            else:
                bookmarked_product_ids = []

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


def contact(request):
    return render(request, "company/contact.html")


def how_it_works(request):
    return render(request, "company/howitworks.html")


def dashboard(request):
    try:
        book_marks=BookMark.objects.filter(user=request.user)
        
      
        reviews_list=Reviews.objects.select_related().filter(reviewed_for=request.user).order_by('-id')[:5]
        
       
        count=book_marks.count()
        context={
            'book_marks':book_marks,
            'count':count,
            'reviews_list':reviews_list
        }
        return render(request, "others/dashboard.html", context)
    except Exception as e:
        print(e)
        # will later redirect to 404 page


def my_listing(request):
    if request.method == "GET":
        sort_option = request.GET.get("sort", "-created_date")  # Default to newest
        products = Product.objects.filter(created_by=request.user).order_by(sort_option)

        paginator = Paginator(products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            data = {
                "products_html": render_to_string(
                    "partials/product_list.html",
                    {"products": page_obj.object_list},
                    request=request,
                ),
            }
            return JsonResponse(data)

        context = {
            "page_obj": page_obj,
            "products": page_obj.object_list,
        }
        return render(request, "others/my-listing.html", context)


def edit_my_listing(request, id):
    product = Product.objects.get(id=id)
    if request.method == "GET":

        features = Feature.objects.all()
        categories = Category.objects.all()
        product_images = ProductImages.objects.filter(product=product)
        selected_categories = product.category.all().values_list("id", flat=True)
        selected_features = product.features.all().values_list("id", flat=True)

        context = {
            "product": product,
            "categories": categories,
            "product_images": product_images,
            "selected_categories": selected_categories,
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

    book_marks = BookMark.objects.filter(user=request.user)

    # paginations added
    paginator = Paginator(book_marks, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"book_marks": page_obj, "page_obj": page_obj, "count": paginator.count}

    return render(request, "others/bookmarks.html", context)


def messages(request):
    return render(request, "others/messages.html")


def reviews(request):
    try:
        visitor_reviews_list = (
            Reviews.objects.select_related()
            .filter(reviewed_for=request.user)
            .order_by("-id")
        )
        your_reviews_list = (
            Reviews.objects.select_related()
            .filter(created_by=request.user)
            .order_by("-id")
        )
        context = {
            "visitor_reviews_list": visitor_reviews_list,
            "your_reviews_list": your_reviews_list,
        }
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

        product_name = request.POST.get("product_name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        tagline = request.POST.get("tagline")
        selected_categories = request.POST.getlist("categories")
        selected_features = request.POST.getlist("features")

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
        )

        # Add selected categories to the product
        for category_id in selected_categories:
            category = Category.objects.get(id=category_id)
            product.category.add(category)

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
        print("Gallery images uploaded")

        return redirect("add_listing")

    else:    
        category=Category.objects.all()
        features=Feature.objects.all()
        context={
            'categories':category,
            'features':features
        }
        return render(request,'listing/add-listing.html',context)



def all_ads(request):
    product_list=Product.objects.all().order_by('-created_date')
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
   return render(request,'others/sub_categories.html')





def search(request):
   
    category_id = request.GET.get('category')
    location = request.GET.get('location')

    products = Product.objects.all().order_by('-id')

    if category_id:
        products = products.filter(category_id=category_id)
    
    if location:
        products = products.filter(location__address__icontains=location)
        
    # Pagination logic
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 1)  # Show 10 products per page
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'category': category_id,
        'location': location,
    }

    return render(request, 'others/search.html', context)
