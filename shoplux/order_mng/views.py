from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from user_product_mng.models import CartItem,Cart
from user_log.models import Address,Account
from product_det.models import Product_Variant
from .models import Order,OrderProduct,Payment
import datetime

# Create your views here.

def place_order(request, total=0, quantity=0):

    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('log:index')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        product_variant = cart_item.product_variant
        if product_variant:  # Check if the product variant exists
            subtotal = product_variant.product.sale_price * cart_item.quantity
            total += subtotal
            quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    try:
         selected_address = request.session.get('selected_address')
         if selected_address:
            address_id = selected_address.get('id')
         address=Address.objects.get(id=address_id)
    except Exception as e:
        print(e)

    print(address)
    print(tax)
    print(grand_total)

    order = Order.objects.create(
        user=request.user,
        address=address,
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


def payment(request, quantity=0, total=0):
    order = Order.objects.get(user=request.user, is_ordered=False)
    cart_items = CartItem.objects.filter(user=request.user)

    # Calculate the total and quantity based on cart items
    for cart_item in cart_items:
        product_variant = cart_item.product_variant
        if product_variant:
            subtotal = product_variant.product.sale_price * cart_item.quantity
            total += subtotal
            quantity += cart_item.quantity

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

    return render(request, 'user_log/success.html')