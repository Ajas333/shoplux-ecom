from django.shortcuts import render,redirect
from .forms import ProductOfferForm
from django.http import HttpResponse,HttpResponseRedirect
from .models import ProductOffer
from product_det.models import Product



# Create your views here.


def add_product_offer(request):
    try:
        product_offers = ProductOffer.objects.all()
    except:
        pass
    if request.method == 'POST':
        form = ProductOfferForm(request.POST, request.FILES)
        if form.is_valid():
            product_offer = form.save()
            product = product_offer.product
            discount=product_offer.discount
            discounted_price = product.sale_price - ((discount / 100) * product.sale_price)
            product.product_offer = discounted_price
            product.save()
            

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  
    else:
        form = ProductOfferForm()
     
    return render(request, 'admin_side/product_offer.html',{'form': form , 'product_offers': product_offers})