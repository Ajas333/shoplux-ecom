from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Account
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
import random
from django.core.exceptions import ObjectDoesNotExist
from product_det.models import Product,Product_Variant
from user_product_mng.models import Cart,CartItem
from user_product_mng.views import _cart_id
import re

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    product=Product.objects.all()
    Product_Variants=Product_Variant.objects.filter(is_active=True)
    context={
        'products':product,
        'product_variants':Product_Variants
    }
       
    return render(request, 'user_log/index.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('log:index')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if not Account.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email Adress")
            return redirect('log:user_login')
        
        if not Account.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "You are blocked by admin ! Please contact admin ")
            return redirect('log:user_login') 

        user = authenticate(request, email=email, password=password)
     

        if user is not None:

            try:
                user_cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                user_cart = Cart.objects.create(cart_id=_cart_id(request))

            # Get anonymous cart items if they exist
            try:
                anonymous_cart_items = CartItem.objects.filter(cart=user_cart)
            except CartItem.DoesNotExist:
                anonymous_cart_items = []

            for item in anonymous_cart_items:
                # Check if the same product variant exists in the user's cart
                existing_item = CartItem.objects.filter(
                    user=user,
                    product_variant=item.product_variant
                ).first()

                if existing_item:
                    # Increment quantity if the same product variant exists
                    existing_item.quantity += item.quantity
                    existing_item.save()
                else:
                    # Otherwise, create a new cart item for the user
                    item.cart = None
                    item.user = user
                    item.save()

            login(request, user)
            messages.success(request, 'You are logged in successfully')
            return redirect('log:index')
        else:
            messages.error(request, 'Login failed. Please check your email and password.')

    return render(request, 'user_log/user_login.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('log:index')
    if request.method=='POST':
        user=request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        
        if not validate_name(user):
             messages.error(request, "Invalid name Format ")
             return redirect('log:user_signup')
        if not is_valid_email(email):
             messages.error(request, "Invalid email Format ")
             return redirect('log:user_signup')
        
        if not is_valid_password(password):
             messages.error(request, "Password should contain atleast 8 characters including atleast one special character, one lowercase letter, one uppercase letter and a number ")
             return redirect('log:user_signup')

        if  Account.objects.filter(email=email).exists():
            messages.error(request, "Email Adress already existing")
            return redirect('log:user_signup')
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('log:user_signup')
        user=Account.objects.create_user(email=email, password=password,username=user)
        user.save()
        request.session['email']=email
        return redirect('log:sent_otp')

    else:
       
        return render(request,'user_log/user_signup.html')
    


def sent_otp(request):
    random_num=random.randint(1000,9999)
    print(random_num)
    request.session['OTP_Key']=random_num
    send_mail(
    "OTP AUTHENTICATING shoplux",
    f"{random_num} -OTP",
    "shoplux333@gmail.com",
    [request.session['email']],
    fail_silently=False,
    )
    print(random_num)
    return redirect('log:verify_otp')



def verify_otp(request):
   print("hello......................")
   user=Account.objects.get(email=request.session['email'])
   if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         print(request.session['OTP_Key'],request.POST['otp'])
         user.is_active=False
      else:
         login(request,user)
         messages.success(request, "signup successful!")
         return redirect('log:index')
   return render(request,'user_log/otp_verification.html')


def user_logout(request):
    logout(request)
    return redirect('log:index') 



def forgot_password(request):
    if request.method == "POST":

        email=request.POST["email"]
        pass1=request.POST["password"]
        pass2=request.POST["conf_password"]

        if pass1 != pass2:
            messages.error(request,"Passwords do not match.")
            return redirect('user_log/forgot_password.html')
        try:
            user = Account.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.warning(request, "your user email not available, plese enter a valid email")
        request.session['email']=email
        request.session['password']=pass1
        return redirect('log:sent_otp_forgot_password') 
    else:
         return render(request,'user_log/forgot_password.html')

def sent_otp_forgot_password(request):
   random_num=random.randint(1000,9999)
   request.session['OTP_Key']=random_num
   print(random_num)
   send_mail(
   "OTP AUTHENTICATING shoplux",
   f"{random_num} -OTP",
   "shoplux333@gmail.com",
   [request.session['email']],
   fail_silently=False,
    )
   return redirect('log:verify_otp_forgot_password')

def verify_otp_forgot_password(request):
    user=Account.objects.get(email=request.session['email'])
    if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         print(request.session['OTP_Key'],request.POST['otp'])
        #  user.is_active=True
      else:
         password=request.session['password']
         user.set_password(password)
         user.save()
         login(request,user)
        #  messages.success(request, "password changed successfully!")
         return redirect('log:user_login')
    return render(request,'user_log/otp_verification.html')


   

#    validation

def validate_name(name):
    name = name.strip()

    if not name:
        return False
    pattern = r'^[A-Za-z\s]+$'

    # Check if the name matches the pattern
    if re.match(pattern, name):
        return True
    else:
        return False

def is_valid_email(email):

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    match = re.match(email_pattern, email)

    return bool(match)


def is_valid_password(password):

    if len(password) < 8:
        return False

    if not re.search(r'[A-Z]', password):
        return False

    if not re.search(r'[a-z]', password):
        return False

    if not re.search(r'\d', password):
        return False

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False

    return True