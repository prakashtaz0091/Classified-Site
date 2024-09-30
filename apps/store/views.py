import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.models import Account
from apps.home.models import Reviews
from apps.store.models import BookMark, Product, ProductImages


# Create your views here.
def service_details(request, product_slug):
    try:
        product_instance = Product.objects.filter(slug=product_slug,is_available=True,is_approved=True).first()
        product_instance.view_count += 1
        product_instance.save()
        if product_instance is None:
            raise Exception("Product with the provided slug is not found")
        product_images = ProductImages.objects.filter(product=product_instance)
        bookmarked_product_ids = None
        processed_featured_data = []
        if product_instance.featured_data:
            for item in product_instance.featured_data:
                if ":" in item:
                    key, value = item.split(":", 1)
                    processed_featured_data.append({'title': key.strip(), 'value': value.strip()})
                else:
                    processed_featured_data.append({'title': item.strip(), 'value': ''})


        if request.user.is_authenticated:
            bookmarked_product_ids = BookMark.objects.filter(
                user=request.user
            ).values_list("product_id", flat=True)

            print(product_instance.featured_data)
        else:
            bookmarked_product_ids = []

        #For showing total ads of that user
        ads_count=Product.objects.filter(created_by=product_instance.created_by).count()
        unique_email_prefix_part=product_instance.created_by.email.split('@')[0]
        
        
        print(product_instance,'product instance display')
        context = {
            "product": product_instance,
            "product_images": product_images,
            "book_mark": bookmarked_product_ids,
            'featured_data':processed_featured_data,
            'ads_count':ads_count,
            'prefix_email':unique_email_prefix_part

        }
        return render(request, "home/service-details.html", context)
    except Exception as e:
        print(e)
        # will later redirect to 404 pages
        return str(e)


@login_required(login_url="/account/login/")
@csrf_exempt
def toggle_bookmark(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get("id")
            product = get_object_or_404(Product, id=product_id)
            bookmark, created = BookMark.objects.get_or_create(
                user=request.user, product=product
            )

            if not created:
                bookmark.delete()
                return JsonResponse({"success": True})

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)


import base64


def decode_id(encoded_id):
    try:
        decoded_string = base64.b64decode(encoded_id).decode("utf-8")
        print(decoded_string,"jl")
        user_id = decoded_string.split(":")[0]  # Extract userId
        return user_id
    except (base64.binascii.Error, UnicodeDecodeError):
        return None


@csrf_exempt
def add_review(request):
    try:
        data = json.loads(request.body)
        print(data)
        feedback = data.get("feedback")
        rating = data.get("rating", "")
        if rating == "":
            rating = 0
        reviewed_for = Account.objects.filter(
            id=(decode_id(data.get("reviewed_for")))
        ).first()
        created_by = Account.objects.filter(id=data.get("created_by")).first()

        Reviews.objects.create(
            review=feedback,
            rating=rating,
            reviewed_for=reviewed_for,
            created_by=created_by,
        )
        return JsonResponse({"status": True, "message": "Review Added Successfully"})
    except Exception as e:
        print(e)
