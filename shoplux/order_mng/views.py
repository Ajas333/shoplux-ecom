from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from user_product_mng.models import CartItem,Cart
from user_log.models import Address,Account
from product_det.models import Product_Variant
from .models import Order,OrderProduct,Payment,OrderAddress
from django.views.decorators.cache import cache_control
import datetime
from django.db.models import Max
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request, total=0, quantity=0):

    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
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
                subtotal = product_variant.product.sale_price * cart_item.quantity
                total += subtotal
                quantity += cart_item.quantity

    if out_of_stock_items:
       
        for item_name in out_of_stock_items:
            messages.error(request, f"Sorry, {item_name} is out of stock.")
        cart_items.filter(product_variant__stock=0).delete()  
        return redirect('log:index') 

    tax = (2 * total) / 100
    grand_total = total + tax

    try:
         selected_address = request.session.get('selected_address')
         if selected_address:
            address_id = selected_address.get('id')
            print('haiiiiiiiiii')
            print(address_id)
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
    
    print('address before save order ')
    print(address)
    print('address after save order ')
    print(new_address)
   
    order = Order.objects.create(
        user=request.user,
        address=new_address,
        order_total=grand_total,
        tax=tax,
        ip=request.META.get('REMOTE_ADDR')

    )
    order.save()
    yr=int(datetime.date.today().strftime('%Y'))
    dt=int(datetime.date.today().strftime('%d'))
    mt=int(datetime.date.today().strftime('%m'))
    d= datetime.date(yr, mt, dt)
    current_date= d.strftime("%Y%m%d")

    order_number=current_date + str(order.id)

    order.order_id = order_number
    order.save()

    context={
        'address':address,
        'grand_total':grand_total,
        'tax':tax,
        'total':total,
        'cart_items':cart_items
    }

    return render(request,'user_log/conform_order.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='log:user_login')
def payment(request, quantity=0, total=0):
   
    order = Order.objects.get(user=request.user, is_ordered=False)
    cart_items = CartItem.objects.filter(user=request.user)
    
    
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
    grand_total = total + tax

    # Create a payment object
    payment = Payment.objects.create(
        user=request.user,
        payment_method="cash on delivery",
        amount_paid=grand_total,
    )

    
    for item in cart_items:
        order_product = OrderProduct()
        order_product.order = order  # Assign the 'order' instance directly
        order_product.payment = payment  # Assign the 'payment' instance directly
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

    CartItem.objects.filter(user=request.user).delete()
    
    try:
        if order.is_ordered == False:
            order.is_ordered = True
    except ValueError:
        pass
    order.save()
    request.session['order_id']=order.id
    return redirect('order_mng:success')

def success(request):
    try:
        order_id=request.session.get('order_id')
        new_order=Order.objects.get(id=order_id)
    except Exception as e:
        print(e)
    
    
    context={
        'new_order':new_order
    }
    
    return render(request,'user_log/success.html',context)

def invoice(request,order_id,total=0):
    try:
        order=Order.objects.get(id=order_id)
        orders=OrderProduct.objects.filter(order=order)
    except:
        pass
    grand_total=0
    for item in orders:
        item.subtotal=item.quantity * item.product_price
        total += item.subtotal
    tax=order.tax
    grand_total = tax + total
    context={
        'order':order,
        'orders':orders,
        'grand_total':grand_total,
        'tax':tax,
    }
    return render(request,'user_log/bill.html',context) 