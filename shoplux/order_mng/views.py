from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from user_product_mng.models import CartItem,Cart
from user_log.models import Address,Account,Wallet,WalletHistory
from Coupon_Mng.models import Coupon
from product_det.models import Product_Variant
from .models import Order,OrderProduct,Payment,OrderAddress
from django.views.decorators.cache import cache_control
import datetime
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal
import razorpay

# Create your views here.
@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request, total=0, quantity=0):

    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    if not cart_items.exists():  
        return redirect('log:index')
    first_cart_item = CartItem.objects.filter(user=current_user).first()
    cart=Cart.objects.get(cart_id=first_cart_item.cart.cart_id)
    coupen_id=cart.coupen
    request.session['coupen_id']=coupen_id.id if coupen_id else None
    cart_count=cart_items.count()
    try:
        
        if cart.coupen is None:

            discount=cart.coupen.discount_rate
    except:
        pass
    if cart_count<=0:
        return redirect('log:index')
    
    grand_total = 0
    tax = 0
    out_of_stock_items = []
    for cart_item in cart_items:
        product_variant = cart_item.product_variant
        if product_variant:
            if product_variant.stock == 0:
                out_of_stock_items.append(product_variant.product.product_name)
            else:
                try:  
                   if product_variant.product.product_offer is not None and product_variant.product.product_offer > 0:
                      subtotal = product_variant.product.product_offer * cart_item.quantity
                   else:
                      subtotal = product_variant.product.sale_price * cart_item.quantity
                except:
                      subtotal = product_variant.product.sale_price * cart_item.quantity
                total += subtotal
                quantity += cart_item.quantity

    if out_of_stock_items:
       
        for item_name in out_of_stock_items:
            messages.error(request, f"Sorry, {item_name} is out of stock.")
        cart_items.filter(product_variant__stock=0).delete()  
        return redirect('log:index') 
    
    tax = (2 * total) / 100
    if coupen_id is not None:
        coupen=Coupon.objects.get(coupon_id=coupen_id)
        discount=coupen.discount_rate
        grand_total=(total + tax ) - discount
    else:
        grand_total = total + tax
    request.session['grand_total'] = float(grand_total)
    request.session['tax'] = float(tax)
    
    try:
         selected_address = request.session.get('selected_address')
         if selected_address:
            address_id = selected_address.get('id')
         address=Address.objects.get(id=address_id)
         Order_Address=OrderAddress.objects.create(
             id=address.id,
             house_name=address.house_name,
             streat_name=address.streat_name,
             post_office=address.post_office,
             place=address.place,
             district=address.district,
             state=address.state,
             country=address.country,
             pincode=address.pincode
         )
         Order_Address.save()
    except Exception as e:
        print(e)
    
    new_address=OrderAddress.objects.get(id=address_id)
    request.session['new_address']=new_address.id

    context={
        'address':address,
        'grand_total':grand_total,
        'tax':tax,
        'total':total,
        'cart_items':cart_items
    }
    try:
       if discount is not None:
          context['discount'] = discount
    except:
        pass
    return render(request,'user_log/conform_order.html',context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='log:user_login')
def payment(request, quantity=0, total=0):

    if request.method == "POST": 
        payment_option = request.POST.get('payment_option')
    
   
    cart_items = CartItem.objects.filter(user=request.user)
    new_address=OrderAddress.objects.get(id=request.session.get('new_address'))
    out_of_stock_items=[]

    for cart_item in cart_items:
        product_variant = cart_item.product_variant
        if product_variant and product_variant.stock < cart_item.quantity:
            out_of_stock_items.append(product_variant.product.product_name)
        else:
            subtotal = product_variant.product.sale_price * cart_item.quantity
            total += subtotal
            quantity += cart_item.quantity

    if out_of_stock_items:
       
        for item_name in out_of_stock_items:
            messages.error(request, f"Sorry, {item_name} is out of stock.")
        cart_items.filter(product_variant__stock=0).delete()
        return redirect('log:index')
    
    tax = (2 * total) / 100
    coupen_id=request.session.get('coupen_id')
    if coupen_id is not None:
        coupen=Coupon.objects.get(id=coupen_id)
        
    grand_total=request.session.get('grand_total')

   
    order = Order.objects.create(
        user=request.user,
        address=new_address,
        order_total=grand_total,
        tax=request.session.get('tax'),
        ip=request.META.get('REMOTE_ADDR'),
    )
    if coupen_id is not None:
        order.coupen=coupen
    yr=int(datetime.date.today().strftime('%Y'))
    dt=int(datetime.date.today().strftime('%d'))
    mt=int(datetime.date.today().strftime('%m'))
    d= datetime.date(yr, mt, dt)
    current_date= d.strftime("%Y%m%d")

    order_number=current_date + str(order.id)

    order.order_id = order_number
    order.save()

    existing_order_products = OrderProduct.objects.filter(order=order)
    if not existing_order_products.exists():
        for item in cart_items:
            order_product = OrderProduct()
            order_product.order = order  # Assign the 'order' instance directly
            order_product.user = request.user
            order_product.product_variant = item.product_variant
            order_product.color = item.color.atribute_value
            order_product.size = item.size.atribute_value
            order_product.quantity = item.quantity
            order_product.product_price = item.product_variant.product.sale_price
            order_product.ordered = True
            order_product.save()
            product_variant=Product_Variant.objects.get(id=item.product_variant.id)
            product_variant.stock -= item.quantity
            product_variant.save()

    request.session['order_id']=order.id
    if payment_option == "cash_on_delivery":
        try:
            if order.is_ordered == False:
                order.is_ordered = True

                payment=Payment.objects.create(
                    user=request.user, 
                    payment_method='Cash on Delivery',
                    Payment_id='COD'
                )
                order.payment=payment
                CartItem.objects.filter(user=request.user).delete()
        except ValueError:
            pass
        order.save()
       
        return redirect('order_mng:success')
    
    elif  payment_option == "wallet": 
        try: 
            wallet=Wallet.objects.get(user=request.user)
            if grand_total < wallet.balance:
                try:
                    if order.is_ordered == False:
                        order.is_ordered = True

                        payment=Payment.objects.create(
                            user=request.user, 
                            payment_method='Wallet',
                            Payment_id='wlt'
                        )
                        order.payment=payment
                        order.save()
                        wallet.balance -= grand_total
                        wallet.save()
                        WalletHistory.objects.create(
                            wallet=wallet,
                            type='Debit',
                            amount=grand_total
                        )

                        CartItem.objects.filter(user=request.user).delete()
                        return redirect('order_mng:success')
                      
                except ValueError:
                    pass
            else:
                messages.error(request,'wallet balance less than total amount')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            
        except ValueError:
            pass
        

    elif payment_option == "razorpay":
            discounted_total = float(grand_total)
            request.session['discounted_total'] = discounted_total
            discounted_total = int(discounted_total * 100)

            client = razorpay.Client(auth=("rzp_test_6HsuV5NiUVTbD7", "y3RXbnznWCtaYRFOq1CFuNdS"))

            DATA = {
                "amount": int(discounted_total),
                "currency": "INR",
                "payment_capture":'1'
                
            }
            client.order.create(data=DATA)

            return render(request,"user_log/razorpay.html", {"grand_total":discounted_total})       
    
       
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def success(request):
    try:
        order_id=request.session.get('order_id')
        new_order=Order.objects.get(id=order_id)
        request.session['stored_order_id'] = new_order.id
        
    except Exception as e:
        print(e)
    
    

    context={
        'new_order':new_order
    }
    
    return render(request,'user_log/success.html',context)


def create_order(request):
    order_id=request.session.get('order_id')
    order=Order.objects.get(id=order_id)
    try:
        if order.is_ordered == False:
            order.is_ordered = True
            payment=Payment.objects.create(
                    user=request.user, 
                    payment_method='razorpay',
                    Payment_id='rzp'
                )
            order.payment=payment
            order.save()
            CartItem.objects.filter(user=request.user).delete()
        else:
            pass
    except ValueError:
            pass
    
    return redirect('order_mng:success')



def invoice(request,order_id,total=0):
    try:
        order=Order.objects.get(id=order_id)
        coupen_id=order.coupen
        orders=OrderProduct.objects.filter(order=order)
    except:
        pass
    if coupen_id is not None:
        coupen=Coupon.objects.get(coupon_id=coupen_id)
        descount=coupen.discount_rate
    grand_total = order.order_total
    for item in orders:
        item.subtotal=item.quantity * item.product_price
        total += item.subtotal
    tax=order.tax
    # if coupen_id is not None:
    #     grand_total =Decimal(tax + total) - descount
    #     # descount_total=grand_total - descount
    # else:
    #     grand_total = tax + total

    context={
        'order':order,
        'orders':orders,
        'grand_total':grand_total,
        'tax':tax,
    }
    try:
       if descount is not None:
          context['descount'] = descount
    except:
        pass
    return render(request,'user_log/bill.html',context) 


