from django.contrib import admin
from django.urls import path
from user_log import views

app_name = 'log'

urlpatterns = [
   path('',views.index,name='index'),
   path('shop',views.shop,name='shop'),
   path('cat_filter/<int:cat_id>/',views.cat_filter,name='cat_filter'),
   path('user_login',views.user_login,name='user_login'),
   path('user_signup',views.user_signup,name='user_signup'),
   path('user_logout',views.user_logout,name='user_logout'),
   path('sent_otp',views.sent_otp,name='sent_otp'),
   path('verify_otp',views.verify_otp,name='verify_otp'),


   path('forgot_password',views.forgot_password,name='forgot_password'),
   path('sent_otp_forgot_password',views.sent_otp_forgot_password,name='sent_otp_forgot_password'),
   path('verify_otp_forgot_password',views.verify_otp_forgot_password,name='verify_otp_forgot_password'),

   path('contact_page',views.contact_page,name='contact_page'),
   path('about',views.about,name='about'),



]
