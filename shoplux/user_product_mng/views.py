from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from product_det.models import Product,Product_Variant,Atribute_Value
from collections import defaultdict
from django.contrib import messages
from .models import Cart,CartItem
from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,Count
from django.http import JsonResponse


def handle_color_selection(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        color_id = request.POST.get('color_id')
        request.session['color_id'] = color_id
       
        return JsonResponse({'color_id': color_id})
    


def variant_color(request, product_id, varient_size):
    product = Product.objects.select_related('product_brand').get(id=product_id)
    product_variants = Product_Variant.objects.filter(product_id=product_id, atributes__id=varient_size)
    color_attribute_values = Atribute_Value.objects.filter(
        Q(attributes__in=product_variants),
        atribute__atribute_name='colour'
    ).distinct()
    
    return color_attribute_values

def product_details(request, product_id,size_id):
    
    product = Product.objects.select_related('product_brand').get(id=product_id)
    product_variants = Product_Variant.objects.filter(product_id=product_id)
    
    color_id = request.session.get('color_id')
    size_attribute_values = Atribute_Value.objects.filter(atribute__atribute_name='size').distinct()
    try:
        if size_id == 0:
            varient_size=size_attribute_values.first().id if size_attribute_values.exists() else 0
        else:
            varient_size=size_id
        request.session['variant_size']=varient_size
    except ValueError:
        pass
    
    desplay_product = variant_color(request, product_id, varient_size)
    context = {
        'product': product,
        'size_attribute_values': size_attribute_values,
        'product_variants': product_variants,
        'desplay_product':desplay_product,
        'varient_size':varient_size,
        'color_id':color_id,
    }
    
    return render(request, 'user_log/product_detail.html', context)





def cart(request, total=0, quantity=0, cart_item=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        if not cart_items:
            messages.error(request, "Your cart is empty")
            return redirect('log:index')
    except ValueError:
        pass
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            # Assuming there's a relationship between CartItem and Product_Variant through product_variant
            product_variant = cart_item.product_variant
            if product_variant:  # Check if the product variant exists
                subtotal = product_variant.product.sale_price * cart_item.quantity
                total += subtotal
                quantity += cart_item.quantity
            
            
        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        
        
    }
    return render(request, 'user_log/shop_cart.html', context)

def _cart_id(request):
     cart=request.session.session_key
     if not cart:
          cart = request.session.create()
     return cart


def add_cart(request, product_id, varient_size):
    color_id = request.session.get('color_id')
    
    product = Product.objects.get(id=product_id)
    
    # Fetch the product variant based on color and size
    product_variant = Product_Variant.objects.filter(
        product=product,
        atributes__in=[color_id, varient_size],
    ).annotate(num_attributes=Count('atributes')).filter(num_attributes=2).first()

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        # Check if the product variant exists and create/update the cart item
        if product_variant:
            cart_item = CartItem.objects.get(product_variant=product_variant, cart=cart)
            try:
                if cart_item.product_variant.stock > cart_item.quantity:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    messages.error(request,"Stock limit reached. Cannot add more to cart")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except ValueError:
                pass
        else:
            # Handle case when product variant with given color and size isn't found
            return HttpResponse("Product variant not found....")
    except CartItem.DoesNotExist:
        # Create a new cart item with the found product variant
        if product_variant:
            color_attribute = Atribute_Value.objects.get(id=color_id)
            size_attribute = Atribute_Value.objects.get(id=varient_size)
            cart_item = CartItem.objects.create(
                product_variant=product_variant,
                quantity=1,
                cart=cart,
                color=color_attribute,
                size=size_attribute,
            )
            cart_item.save()
        else:
            # Handle case when product variant with given color and size isn't found
            return HttpResponse("Product variant not found.")
    
    return redirect('user_product:cart')
    
def increment_cart(request, cart_item_id):
    cart_item=get_object_or_404(CartItem, id=cart_item_id)
    print(cart_item)
    try:
        if cart_item.product_variant.stock > cart_item.quantity:
            cart_item.quantity +=1
            cart_item.save()
        else:
            messages.error(request,"Stock limit reached. Cannot add more to cart")
    except ValueError:
        pass
    return redirect('user_product:cart')
    
def remove_cart(request,cart_item_id):
   
    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('user_product:cart')

def remove_cart_item(request,cart_item_id):
     
     cart_item= CartItem.objects.get(id=cart_item_id)
     cart_item.delete()

     return redirect('user_product:cart')
     
     

