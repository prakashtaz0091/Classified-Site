from django.shortcuts import render

#Property landing page
def landing_page(request):
    try:
        return render(request,'business_place/landing.html')
    except Exception as e:
        print(e)
        # will later return to some 400 page
        return e
