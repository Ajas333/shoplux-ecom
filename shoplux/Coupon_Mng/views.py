from django.shortcuts import render,redirect
from .forms import CouponForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()  
            messages.success(request, 'Coupon added successfully.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  
    else:
        form = CouponForm()
    return render(request,'admin_side/coupon_mng.html',{'form': form})