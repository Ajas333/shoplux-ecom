from django.shortcuts import render

# Create your views here.

def add_coupon(request):

    return render(request,'admin_side/coupon_mng.html')