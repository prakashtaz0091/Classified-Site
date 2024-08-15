from django.shortcuts import render

from apps.store.models import Product, ProductImages
from django.contrib.auth.decorators import login_required
from apps.store.models import BookMark
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
    
    
def service_details(request,product_slug):
    try:
        product_instance=Product.objects.filter(slug=product_slug).first()
        product_instance.view_count+=1
        product_instance.save()
        if product_instance is None:
            raise Exception("Product with the provided slug is not found")
        product_images=ProductImages.objects.filter(product=product_instance)
        bookmarked_product_ids=None
        if request.user.is_authenticated:    
                bookmarked_product_ids = BookMark.objects.filter(user=request.user).values_list('product_id', flat=True)
        else: 
                bookmarked_product_ids = []
        print(bookmarked_product_ids)
        context={
            'product':product_instance,
            'product_images':product_images,
                'book_mark':bookmarked_product_ids,
        }
        return render(request,'home/service-details.html',context)    
    except Exception as e:
        print(e)
        # will later redirect to 404 pages
        return str(e)
        



@login_required(login_url='/account/login/') 
@csrf_exempt
def toggle_bookmark(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('id')
            product = get_object_or_404(Product, id=product_id)
            bookmark, created = BookMark.objects.get_or_create(user=request.user, product=product)
            
            if not created:
                bookmark.delete()
                return JsonResponse({'success': True})
            
            return JsonResponse({'success': True})
        
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
