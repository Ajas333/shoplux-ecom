from product_det.models import Category,Brand,Atribute,Atribute_Value,Product,Product_Variant
# from user_log.models import Account,AccountUser,Address
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout as auth_logout
from user_log.forms import AddressForm
from user_log.models import Address,Account
from order_mng.models import Order,OrderProduct,OrderAddress
from django.urls import reverse


def user_profile(request,user_id):
    form = AddressForm()
    account = get_object_or_404(Account, id=user_id)
    addresses = Address.objects.filter(account=account)
    orders=Order.objects.filter(user=request.user)
    print(orders)
    context={
        'form':form,
        'addresses':addresses,
        'orders':orders
     
    }
    return render(request,'user_log/profile.html',context)


def edit_user(request,user_id): 

    accounts=Account.objects.get(id=user_id)
    try:
        if request.method == 'POST':
            accounts.username=request.POST.get('user_name')
            accounts.email=request.POST.get('user_email')
            accounts.phone=request.POST.get('user_phone')
            try:
                accounts.image=request.FILES['image_feild'] 
            except:
                pass
            accounts.save()
            return redirect('user_area:user_profile',user_id=user_id)
            

    except ValueError:
        pass
    context={
        'accounts':accounts
    }


    return render(request,'user_log/edit_user.html',context)



@login_required
def change_password(request,user_id):

    user=Account.objects.get(id=user_id)
    if request.method == 'POST':
        
        old_pass=request.POST.get('pass')
        pass1=request.POST.get('npass')
        pass2=request.POST.get('cpass')

        try:
            if check_password(old_pass, user.password):
                if pass1 == pass2: 
                    user.set_password(pass1)
                    user.save()
                    messages.success(request, 'Password changed successfully.')
                    return redirect('log:user_login')
                else:
                    messages.error(request, 'New passwords do not match.')
                    
            else:
                messages.error(request, 'Incorrect old password.')
                
        except Exception as e:
                messages.error(request, 'An error occurred while changing the password.')
                # Log the exception for debugging
                print(e)
            
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def logout(request):
    auth_logout(request)
    return redirect('log:index') 


def add_address(request,user_id):

    account = get_object_or_404(Account, id=user_id)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address_instance = form.save(commit=False)
            address_instance.account = account  # Set the account for the address
            address_instance.save()

            messages.success(request, 'Address added successfully.')
            return HttpResponseRedirect(reverse('user_area:user_profile', args=[request.user.id]))
        else:
            messages.error(request, 'Invalid form data. Please check the entered information.')
    else:
        form = AddressForm()
    return render(request, 'user_log/profile.html', {'form': form})


def edit_address(request, address_id):
   
    address = Address.objects.get(id=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully.')
            return HttpResponseRedirect(reverse('user_area:user_profile', args=[request.user.id]))
        else:
            messages.error(request, 'Invalid form data. Please check the entered information.')
    else:
        form = AddressForm(instance=address)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def set_default_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    account = address.account 
    try:
        address = Address.objects.get(id=address_id)
        Address.objects.filter(account=account).exclude(pk=address_id).update(is_default=False)
        address.is_default = True
        address.save()
    except Address.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('user_area:user_profile', args=[request.user.id]))


def order_details(request,order_id, total=0, quantity=0):
    
    order=Order.objects.get(id=order_id)
    order_items=OrderProduct.objects.filter(order=order_id)
    print(order_items)

    address=order.address
    print(address)
    
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
        
    context={
        'order':order,
        'address':address,
        'order_items':order_items,
        'tax':tax,
        'grand_total':grand_total
       
    }
    return render(request,'user_log/order_details.html',context)