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
from product_det.models import Product

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    product=Product.objects.all()
    context={
        'products':product
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
            login(request, user)
            # messages.success(request, 'You are logged in successfully')
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


   