from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.cache import cache_control
from product_det.models import Product,Product_Variant,Atribute_Value
from user_log.models import Address
from Coupon_Mng.models import Coupon
from collections import defaultdict
from django.contrib import messages
from .models import Cart,CartItem,Wishlist,WishlistItems
from django.http import HttpResponse,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import datetime
from user_log.forms import AddressForm
from user_log.models import Account
from django.urls import reverse


def handle_color_selection(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        color_id = request.POST.get('color_id')
        request.session['color_id'] = color_id
       
        return JsonResponse({'color_id': color_id})
    


def variant_color(request, product_id, varient_size):
    # product = Product.objects.select_related('product_brand').get(id=product_id)
    product_variants = Product_Variant.objects.filter(product_id=product_id, atributes__id=varient_size)
    color_attribute_values = Atribute_Value.objects.filter(
        Q(attributes__in=product_variants),
        atribute__atribute_name='colour'
    ).distinct()
    
    return color_attribute_values

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart(request, total=0, quantity=0, cart_item=None):
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
       
    except ObjectDoesNotExist:
        cart_items = []  
        tax = grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        try:
            if request.method=="POST":
               coupen_code=request.POST.get('coupon_code')
               try:
                   coupon = Coupon.objects.get(coupon_id=coupen_code)
                
                   if coupon.is_active:
                       Coupen_org=Coupon.objects.get(coupon_id=coupon)
                       descount=coupon.discount_rate
                       cart.coupen=Coupen_org
                       cart.save()
                       messages.success(request, 'Coupon applied successfully!')
                   else:
                       messages.error(request, 'Coupon has expired')
               except Coupon.DoesNotExist:
                   messages.error(request, 'Invalid coupon code')
            
        except:
            pass
        for cart_item in cart_items:
            
            product_variant = cart_item.product_variant
            if product_variant:
                try:  
                   if product_variant.product.product_offer is not None and product_variant.product.product_offer > 0:
                      subtotal = product_variant.product.product_offer * cart_item.quantity
                   else:
                       subtotal = product_variant.product.sale_price * cart_item.quantity
                except:
                     subtotal = product_variant.product.sale_price * cart_item.quantity
                
                total += subtotal
                quantity += cart_item.quantity

        tax = (2 * total) / 100
        try:
            if descount:
               grand_total=(total + tax) - descount  
        except:  
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
    try:
       if descount is not None:
          context['descount'] = descount
    except:
        pass
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

    # Check if the product variant exists
    if product_variant:
        # Check if the product variant stock is greater than zero
        if product_variant.stock > 0:
            try:
                cart_item = CartItem.objects.get(product_variant=product_variant, cart=cart)
                if cart_item.product_variant.stock > cart_item.quantity:
                    cart_item.quantity += 1
                    cart_item.save()
                else:
                    messages.error(request,"Stock limit reached. Cannot add more to cart")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            except CartItem.DoesNotExist:
                if request.user.is_authenticated:
                    existing_cart_item = CartItem.objects.filter(
                            user=request.user,
                            product_variant=product_variant
                        ).first()
                    if existing_cart_item:
                        if existing_cart_item.product_variant.stock > existing_cart_item.quantity:
                            existing_cart_item.quantity += 1
                            existing_cart_item.save()
                        else:
                            messages.error(request, "Stock limit reached. Cannot add more to cart")
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                    else:
                        color_attribute = Atribute_Value.objects.get(id=color_id)
                        size_attribute = Atribute_Value.objects.get(id=varient_size)
                        cart_item = CartItem.objects.create(
                            product_variant=product_variant,
                            quantity=1,
                            cart=cart,
                            color=color_attribute,
                            size=size_attribute,
                            user=request.user
                        )
                        cart_item.save()
                else:
                    color_attribute = Atribute_Value.objects.get(id=color_id)
                    size_attribute = Atribute_Value.objects.get(id=varient_size)
                    cart_item = CartItem.objects.create(
                        product_variant=product_variant,
                        quantity=1,
                        cart=cart,
                        color=color_attribute,
                        size=size_attribute
                    )
                    cart_item.save()
        else:
            messages.error(request, "Product out of stock. Cannot add to cart.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # Handle case when product variant with given color and size isn't found
        messages.error(request,"Pleas select color")
        return redirect('user_product:product_details', product_id=product_id, size_id=varient_size)

        
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    
def increment_cart(request, cart_item_id):
    cart_item=get_object_or_404(CartItem, id=cart_item_id)
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
     
     

@login_required(login_url='log:user_login')
def checkout(request, total=0, quantity=0, cart_item=None):
    if not request.user.is_authenticated:
        return redirect('log:user_login')
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        form = AddressForm()
       
    except ObjectDoesNotExist:
        cart_items = []  
        tax = grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:

            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

       
        if request.user.is_authenticated:
            current_user=request.user
        addresses=Address.objects.filter(account=current_user)
       
        for cart_item in cart_items:
           
            product_variant = cart_item.product_variant
            if product_variant and product_variant.stock == 0:
                messages.error(request, f"Sorry, {product_variant.product.product_name} is out of stock.")
                CartItem.objects.filter(cart=cart, product_variant=product_variant).delete() 
                return redirect('log:index') 
            try:  
                if product_variant.product.product_offer is not None and product_variant.product.product_offer > 0:
                   subtotal = product_variant.product.product_offer * cart_item.quantity
                else:
                   subtotal = product_variant.product.sale_price * cart_item.quantity
            except:
                   subtotal = product_variant.product.sale_price * cart_item.quantity
                
            total += subtotal
            quantity += cart_item.quantity
            
        tax = (2 * total) / 100
        try:
            coupen=cart.coupen.coupon_id
            descount=cart.coupen.discount_rate
            if cart.coupen.is_active:
                grand_total = (total + tax) - descount
            else:
                messages.error(request,'coupen expired')
        except:
             grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    if request.POST.get('address_id'):
        address_id=request.POST.get('address_id')
        try:
            address=Address.objects.get(id=address_id)
        except Exception as e:
            print(e)
    else:
        address=addresses.filter(is_default=True).first()
    try:
        request.session['selected_address'] = {
            'id': address.id,
        }
    except:
        messages.error(request,"add address")
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'addresses':addresses,
        'address':address,
        'form':form,
    }
    try:
       if descount is not None:
          context['descount'] = descount
    except:
        pass
    return render(request,'user_log/shop_checkout.html',context)



@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_address_checkout(request,user_id):

    account = get_object_or_404(Account, id=user_id)
    existing_addresses = Address.objects.filter(account=account)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address_instance = form.save(commit=False)
            address_instance.account = account  
            if not existing_addresses.exists(): 
                address_instance.is_default = True
            address_instance.save()

            messages.success(request, 'Address added successfully.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, 'Invalid form data. Please check the entered information.')
    else:
        form = AddressForm()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def wishlist(request):
    if not request.user.is_authenticated:
        messages.info(request,'login to access wishlist')
        return redirect('log:user_login')
    else:
        try:
            wishlist=Wishlist.objects.get(user=request.user)
            wishlist_items=WishlistItems.objects.filter(wishlist=wishlist)
            context={
                'wishlist_items':wishlist_items
            }
        except:
            pass
    return render(request,'user_log/wishlist.html',context)


def add_wishlist(request,product_id):
    if not request.user.is_authenticated:
        messages.info(request,'login to access wishlist')
        return redirect('log:user_login')
    else:
        try:
            wishlist=Wishlist.objects.get(user=request.user)
           
        except:
            wishlist=Wishlist.objects.create(user=request.user)
            

        product=get_object_or_404(Product,id=product_id)

        if WishlistItems.objects.filter(wishlist=wishlist, product=product).exists():
            messages.info(request, 'Product is already in your wishlist')
        else:
            WishlistItems.objects.create(wishlist=wishlist, product=product)
            messages.success(request, 'Product added to your wishlist successfully')
        
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delete_wishlist(request,wishlit_item_id):

    item=get_object_or_404(WishlistItems,id=wishlit_item_id)
    item.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))