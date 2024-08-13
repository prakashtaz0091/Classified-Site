from django.shortcuts import render

from apps.category.models import Category
from apps.store.models import Product

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
            context = {
                'latest_products': latest_products,
                'categories':all_categories
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
    return render(request,'others/dashboard.html')




def profile(request):
    return render(request,'others/profile.html')



def my_listing(request):
    return render(request,'others/my-listing.html')



def book_marks(request):
    return render(request,'others/booksmarks.html')


def messages(request):
    return render(request,'others/messages.html')


def reviews(request):
    return render( request,'others/reviews.html')