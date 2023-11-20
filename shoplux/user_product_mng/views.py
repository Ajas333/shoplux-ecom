from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from product_det.models import Product,Product_Variant
from collections import defaultdict
from product_det.models import Product
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


def product_details(request,product_id):
    product = Product.objects.select_related('product_brand').get(id=product_id)
    product_variants=Product_Variant.objects.filter(product_id=product_id)
    attribute_values_dict ={}
    for variant in product_variants:
            attributes = variant.atributes.all()  # Accessing attributes of the variant
            for attribute in attributes:
                attribute_name = attribute.atribute.atribute_name
                attribute_value = attribute.atribute_value
                if attribute_name not in attribute_values_dict:
                    attribute_values_dict[attribute_name] = {attribute_value}
                else:
                    attribute_values_dict[attribute_name].add(attribute_value)

    print(attribute_values_dict)
    context={
        'product':product,
        'attribute_values_dict': attribute_values_dict
    }
    
    return render(request, 'user_log/product_detail.html',context)


def cart(request, total=0, quantity=0, cart_item=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
             total += (cart_item.product.sale_price * cart_item.quantity)
             quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
         pass
    context={
         'total':total,
         'quantity':quantity,
         'cart_items':cart_items,
         'tax':tax,
         'grand_total':grand_total,
    }
    return render(request,'user_log/shop_cart.html',context)

def _cart_id(request):
     cart=request.session.session_key
     if not cart:
          cart = request.session.create()
     return cart


def add_cart(request,product_id):   
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
         cart=Cart.objects.create(
              cart_id=_cart_id(request)
         )
    cart.save()

    try:
        cart_item=CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
         cart_item = CartItem.objects.create(
              product=product,
              quantity = 1,
              cart = cart,
         )
         cart_item.save()
    
    return redirect('user_product:cart')
    
def remove_cart(request,product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('user_product:cart')

def remove_cart_item(request,product_id):
     cart = Cart.objects.get(cart_id=_cart_id(request))
     product= get_object_or_404(Product, id=product_id)
     cart_item= CartItem.objects.get(product=product, cart=cart)
     cart_item.delete()

     return redirect('user_product:cart')
     
     

