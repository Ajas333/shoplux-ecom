from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from product_det.models import Product,Product_Variant,Atribute_Value
from collections import defaultdict
from product_det.models import Product
from .models import Cart,CartItem
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q



def variant_color(request, product_id, varient_size):
    product = Product.objects.select_related('product_brand').get(id=product_id)
    product_variants = Product_Variant.objects.filter(product_id=product_id, atributes__id=varient_size)
    color_attribute_values = Atribute_Value.objects.filter(
        Q(attributes__in=product_variants),
        atribute__atribute_name='colour'
    ).distinct()
    # print(color_attribute_values)
    # print(product_variants)
    print(varient_size)
    desplay_product = product_variants[0]
    return color_attribute_values

def product_details(request, product_id,size_id):
    print(size_id)
    product = Product.objects.select_related('product_brand').get(id=product_id)
    product_variants = Product_Variant.objects.filter(product_id=product_id)
    

    size_attribute_values = Atribute_Value.objects.filter(atribute__atribute_name='size').distinct()
    try:
        if size_id == 0:
            varient_size=size_attribute_values.first().id if size_attribute_values.exists() else 0
        else:
            varient_size=size_id
    except ValueError:
        pass
    # size_id = size_attribute_values.first().id if size_attribute_values.exists() else 0
    
    # Pass the size_id to variant_color function
    desplay_product = variant_color(request, product_id, varient_size)
    # print(desplay_product)
    
    context = {
        'product': product,
        'size_attribute_values': size_attribute_values,
        'product_variants': product_variants,
        'desplay_product':desplay_product
    }
    
    return render(request, 'user_log/product_detail.html', context)





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
     
     

