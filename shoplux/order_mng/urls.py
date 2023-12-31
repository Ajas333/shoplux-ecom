from django.urls import path
from order_mng import views

app_name='order_mng'
urlpatterns = [
    path('place_order',views.place_order,name='place_order'),
    path('payment',views.payment,name='payment'),
    path('success',views.success,name='success'),
    path('invoice/<int:order_id>/',views.invoice,name='invoice'),

    path('create_order',views.create_order,name='create_order')
]

