from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from user_log.models import Account
from order_mng.models import Order,OrderProduct
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from order_mng.forms import OrderForm

# Create your views here.

def admin_login(request):
    if  request.user.is_superuser:
        return redirect('admin_dashboard:dashboard')

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_superuser:
                login(request, user)
                # messages.success(request, "Admin login successful!")
                return redirect('admin_dashboard:dashboard')  # Use the named URL pattern

            messages.error(request, "Invalid admin credentials!")
    return render(request, 'admin_side/admin_login.html')



@login_required(login_url='adminlog:admin_login')  # Use the named URL pattern
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_dashboard(request):
    return render(request,'admin_side/admin_index.html')


def admin_logout(request):
    logout(request)

    return redirect('adminlog:admin_login')

@login_required(login_url='adminlog:admin_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users_list(request):
    if not request.user.is_authenticated:
        return redirect('adminlog:admin_login')
    
    search_query=request.GET.get('query')

    if search_query:
         users = Account.objects.filter(username__icontains=search_query)
    else:
         users = Account.objects.all()
         print("the users are :", users)
    context = {
        'users': users
    }
      
    return render(request,'admin_side/users_list.html',context)


@login_required(login_url='adminlog:admin_login')
def block_unblock_user(request,user_id):
    if not request.user.is_authenticated:
        return HttpResponse("Unauthorized", status=401)
    
    user = get_object_or_404(Account, id=user_id)
    
    if user.is_active:
        
        user.is_active=False
        
    else:
        user.is_active=True
        
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def order_list(request):
    
    orders=Order.objects.all()

    context={
        'orders':orders,
    }

    return render(request,'admin_side/order_details.html',context)


def order_details(request,order_id, total=0, quantity=0):
    print("wwwwwwwwwwwwwwwwwww,    :",order_id)
    try:
        order=Order.objects.get(id=order_id)
    except Exception as e:
        print(e)
    order_items=OrderProduct.objects.filter(order=order)

    address=order.address
    
    grand_total = 0
    tax = 0
    for order_item in order_items:
        product_variant = order_item.product_variant
        if product_variant:  # Check if the product variant exists
            subtotal = product_variant.product.sale_price * order_item.quantity
        
            total += subtotal
            quantity += order_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method=="POST":
        form=OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('adminlog:order_details', order_id = order.pk)
        else:
            messages.error(request, "choose status")
            return redirect('adminlog:order_details', order_id = order.pk)


    form=OrderForm(instance=order)
    
    context={
        'order':order,
        'address':address,
        'order_items':order_items,
        'tax':tax,
        'grand_total':grand_total,
        'total':total,
        'form':form
            }
    return render(request,'admin_side/page_orders_detail.html',context)


def cancell_order(request,order_id):
    print(order_id)
    try:
        order=Order.objects.get(id=order_id)
    except Exception as e:
        print(e)
    
    order.status = 'Cancelled'
    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))