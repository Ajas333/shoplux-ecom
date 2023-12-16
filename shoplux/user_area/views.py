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
from user_log.models import Address,Account,Wallet,WalletHistory
from order_mng.models import Order,OrderProduct,OrderAddress
from Coupon_Mng.models import Coupon
from django.urls import reverse
from django.contrib.auth.decorators import login_required


@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_profile(request,user_id):
    if not request.user.is_authenticated:
        return redirect('log:user_login')

    form = AddressForm()
    account = get_object_or_404(Account, id=user_id)
    wallet=get_object_or_404(Wallet,user=account)
    wallethistory = WalletHistory.objects.filter(wallet=wallet)
    addresses = Address.objects.filter(account=account)
    orders=Order.objects.filter(user=request.user)
    
    context={
        'form':form,
        'addresses':addresses,
        'orders':orders,
        'wallet':wallet,
        'wallethistory':wallethistory,
     
    }
    return render(request,'user_log/profile.html',context)

@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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



@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_address(request,user_id):

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
            return HttpResponseRedirect(reverse('user_area:user_profile', args=[request.user.id]))
        else:
            messages.error(request, 'Invalid form data. Please check the entered information.')
    else:
        form = AddressForm()
    return render(request, 'user_log/profile.html', {'form': form})


def delete_address(request,address_id):

    try:
        address=Address.objects.get(id=address_id)
        address.delete()

        messages.info(request, 'address delete successfully')
    except:
        messages.error(request,'something error happends..')


    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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

@login_required(login_url='log:user_login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_details(request,order_id, total=0, quantity=0):
    
    order=Order.objects.get(id=order_id)
    order_items=OrderProduct.objects.filter(order=order_id)

    address=order.address
    
    grand_total = order.order_total
    tax = 0
    for order_item in order_items:
        product_variant = order_item.product_variant
        if product_variant:  # Check if the product variant exists
            try:  
                if product_variant.product.product_offer is not None and product_variant.product.product_offer > 0:
                      subtotal = product_variant.product.product_offer * order_item.quantity
                else:
                       subtotal = product_variant.product.sale_price * order_item.quantity
            except:
                     pass
                     
           
            total += subtotal
            quantity += order_item.quantity
    tax = (2 * total) / 100
    if order.coupen:
        coupen=Coupon.objects.get(coupon_id=order.coupen)
        descount=coupen.discount_rate
        
    context={
        'order':order,
        'address':address,
        'order_items':order_items,
        'tax':tax,
        'grand_total':grand_total
       
    }
    try:
        if descount is not None:
            context['descount'] = descount
    except:
         pass
    return render(request,'user_log/order_details.html',context)

def cancell(request,order_id):
    try:
        order = Order.objects.get(id=order_id)
        wallet = Wallet.objects.get(user=request.user)

        if order.payment.payment_method == 'Wallet' or order.payment.payment_method == 'razorpay':
            wallet.balance += order.order_total
            wallet.save()
            WalletHistory.objects.create(
                        wallet=wallet,
                        type='Credited',
                        amount=order.order_total
                        )

            refunded_message = f'Amount of {order.order_total} refunded successfully to your wallet.'
            messages.success(request, refunded_message)
        order.status = 'Cancelled'
        order.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    except Exception as e:
        print(e)
       
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def return_order(request,order_id):
    try:
        order = Order.objects.get(id=order_id)
        wallet = Wallet.objects.get(user=request.user)

        wallet.balance += order.order_total
        wallet.save()
        WalletHistory.objects.create(
                    wallet=wallet,
                    type='Credited',
                    amount=order.order_total
                    )

        refunded_message = f'Amount of {order.order_total} refunded successfully to your wallet.'
        messages.success(request, refunded_message)
        order.status = 'Return'
        order.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    except Order.DoesNotExist:
        pass

    except Wallet.DoesNotExist:
      
        pass

    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


