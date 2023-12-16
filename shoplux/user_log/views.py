from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Account,Wallet
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import send_mail
import random
from django.core.exceptions import ObjectDoesNotExist
from product_det.models import Product,Product_Variant,Category
from Offer_mng.models import ProductOffer
from user_product_mng.models import Cart,CartItem
from user_product_mng.views import _cart_id
from django.contrib.auth.decorators import login_required
import re
from django.views.decorators.cache import never_cache

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
   
    product=Product.objects.all()
    Product_Variants=Product_Variant.objects.filter(is_active=True)
    product_offers=ProductOffer.objects.filter(is_active=True)
    for p in product:
       try:
           product_offer=ProductOffer.objects.get(product=p)
           if product_offer.is_active:
              pass
           else:
               p.product_offer = 0
               p.save()
           
       except:
           p.product_offer = 0
           p.save()
    
       
    context={
        'products':product,
        'product_variants':Product_Variants
    }
    if product_offers is not None:
        context['product_offers']=product_offers

    return render(request, 'user_log/index.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def shop(request):
    categories = Category.objects.all()
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(product_name__icontains=query)
        product_count = products.count()
    else:
        products = Product.objects.all()
        product_count = products.count()
    
    product_variants = Product_Variant.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'products': products,
        'product_variants': product_variants,
        'query': query,
        'product_count' : product_count
    }
    return render(request,'user_log/shop.html',context)

def cat_filter(request,cat_id):
    selected_category = get_object_or_404(Category, pk=cat_id)
    products = Product.objects.filter(product_catg=selected_category)
    product_count = products.count()
    
    categories = Category.objects.all()
    product_variants = Product_Variant.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'products': products,
        'product_variants': product_variants,
        'query': "",  # No query for category filtering
        'product_count': product_count
    }
    return render(request,'user_log/shop.html',context)

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
        Wallet.objects.create(
            user=user
        )
        request.session['email']=email
        return redirect('log:sent_otp')

    else:
       
        return render(request,'user_log/user_signup.html')
    


def sent_otp(request):
    random_num=random.randint(1000,9999)
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
   
   user=Account.objects.get(email=request.session['email'])
   if request.method=="POST":
      if str(request.session['OTP_Key']) != str(request.POST['otp']):
         user.is_active=False
      else:
         login(request,user)
         messages.success(request, "signup successful!")
         return redirect('log:index')
   return render(request,'user_log/otp_verification.html')

@never_cache
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

def contact_page(request):

    return render(request, 'user_log/contact_page.html')

def about(request):

    return render(request, 'user_log/about.html')


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