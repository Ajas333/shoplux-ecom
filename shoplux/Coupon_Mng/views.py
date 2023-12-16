from django.shortcuts import render,redirect
from .forms import CouponForm
from.models import Coupon
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def add_coupon(request):
    coupens=Coupon.objects.all()
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Coupon added successfully.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  
    else:
        form = CouponForm()
    
    context={
        'form':form,
        'coupens':coupens,
    }
    return render(request,'admin_side/coupon_mng.html',context)