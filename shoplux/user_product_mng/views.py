from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from product_det.models import Product,Product_Variant


# Create your views here.


def product_details(request,product_id):
    
   product = Product.objects.select_related('product_brand').get(id=product_id)

   context={
        'product':product
    }
    
   return render(request, 'user_log/product_detail.html',context)

