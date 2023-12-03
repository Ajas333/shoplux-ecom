from django.urls import path
from Coupon_Mng import views

app_name='coupon'

urlpatterns = [
    path('add_coupon',views.add_coupon,name='add_coupon'),
]
