from django.shortcuts import render
from django.core.paginator import Paginator
from apps.category.models import Category
from apps.store.models import Product,BookMark

# Create your views here. i am your home


def home(request):
    if request.method == 'GET':
        try:
            all_categories = Category.objects.select_related().all().order_by('-id')
            latest_products = []

            # Get the latest 5 products for each category
            for category in all_categories:
                products = Product.objects.select_related().filter(category=category, is_available=True).order_by('-created_date')[:5]
                latest_product = {'products':products,'category':category}
                latest_products.append(latest_product)
            
            if request.user.is_authenticated:    
                bookmarked_product_ids = BookMark.objects.filter(user=request.user).values_list('product_id', flat=True)
            else: 
                bookmarked_product_ids = []
  
           
            context = {
                'latest_products': latest_products,
                'categories':all_categories,
                'book_mark':bookmarked_product_ids,
            }
           
            return render(request,'home/index.html',context)
        except Exception as e:
            print('error')
            print(e)
            #later redirect to some 404 page with custom error message
            return  "error"





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

# For customers to provide feedback or opinions to user
def feedback(request,hashed_user_id):
    try:

        return render(request,'home/feedback.html')
    except Exception as e:
        print(e)
        #will later move it to 404 page
        return e


