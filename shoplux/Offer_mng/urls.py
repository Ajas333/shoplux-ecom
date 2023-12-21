from django.urls import path
from Offer_mng import views

app_name='offer'

urlpatterns = [
    path('add_product_offer',views.add_product_offer,name='add_product_offer'),
    path('delete_offer/<int:offer_id>/',views.delete_offer,name='delete_offer')
]
