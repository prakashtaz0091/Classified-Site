from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from apps.category.models import Category
from apps.store.models import Product,BookMark,Location,ContactInformation,ProductImages
from django.contrib.auth.decorators import login_required




def home(request):
    if request.method == 'GET':
        try:
            # Fetch all categories
            all_categories = Category.objects.select_related().all().order_by('-id')
            latest_products = []
            all_products = Product.objects.select_related().filter(is_available=True).order_by('-created_date')

            # Get the latest 5 products for each category
            for category in all_categories:
                
                products = Product.objects.select_related().filter(category=category, is_available=True).order_by('-created_date')[:5]
             
                latest_product = {'products': products, 'category': category}
                latest_products.append(latest_product)
            
            # Fetch bookmarked product IDs if the user is authenticated
            if request.user.is_authenticated:    
                bookmarked_product_ids = BookMark.objects.filter(user=request.user).values_list('product_id', flat=True)
            else: 
                bookmarked_product_ids = []
  
            context = {
                'latest_products': latest_products,
                'all_products': all_products,
                'categories': all_categories,
                'book_mark': bookmarked_product_ids,
            }
           
            return render(request, 'home/index.html', context)
        except Exception as e:
            print('Error:')
            print(e)
            # Redirect to a custom error page or return an error response
            return render(request, 'home/error.html', {'error': str(e)})





def privacy(request):
    # return render(request,'company/')
    pass



def freq_question(requset):
    return render(requset,'company/faq.html')


def terms(request):
    return render(request,'company/terms-condition.html')



def contact(request):
    return render(request,'company/contact.html')



def how_it_works(request):
    return render(request,'company/howitworks.html')



def dashboard(request):
    book_marks=BookMark.objects.filter(user=request.user)
    count=book_marks.count()
    context={
        'book_marks':book_marks,
        'count':count
    }
    return render(request,'others/dashboard.html',context)








def my_listing(request):
    
    return render(request,'others/my-listing.html')


def book_marks(request):
   
    book_marks = BookMark.objects.filter(user=request.user)
    
    # paginations added 
    paginator = Paginator(book_marks, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'book_marks': page_obj,  
        'page_obj': page_obj,     
        'count': paginator.count 
    }

    return render(request, 'others/bookmarks.html', context)

def messages(request):
    return render(request,'others/messages.html')


def reviews(request):
    return render( request,'others/reviews.html')




@login_required(login_url='/account/login/') 
def add_listing(request):
    if request.method == 'POST':
       
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        selected_categories = request.POST.getlist('categories')
       
        # Retrieve location data
        location_name = request.POST.get('location')
        address = request.POST.get('address')
        map_address = request.POST.get('map_address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        # Retrieve contact information
        email = request.POST.get('email')
        website = request.POST.get('website')
        phone = request.POST.get('phone')

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
            location=location,
            contact_information=contact_information,
            is_available=True,  
            created_by=request.user
        )
      

        # Add selected categories to the product
        for category_id in selected_categories:
            category = Category.objects.get(id=category_id)
            product.category.add(category)

        # Handle file uploads for cover image
        cover_image = request.FILES.get('cover_image')
        if cover_image:
            product.cover_image = cover_image
            product.save()
            print('Cover image uploaded')

        # Handle file uploads for gallery images
        gallery_images = request.FILES.getlist('gallery_images')
        for image in gallery_images:
            ProductImages.objects.create(product=product, image=image)
        print('Gallery images uploaded')

       
        return redirect('add_listing')


   
    else:    
        category=Category.objects.all()
        context={
            'categories':category
        }
        return render(request,'listing/add-listing.html',context)