from django.urls import path
from user_product_mng import views

app_name='user_product'

urlpatterns = [
    path('product_details/<int:product_id>/',views.product_details,name='product_details')
]
