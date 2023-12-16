from django.urls import path
from user_product_mng import views

app_name='user_product'

urlpatterns = [
    path('product_details/<int:product_id>/<int:size_id>',views.product_details,name='product_details'),

    path('cart',views.cart,name='cart'),
    path('add_cart/<int:product_id>/<int:varient_size>',views.add_cart,name='add_cart'),
    path('increment_cart/<int:cart_item_id>/',views.increment_cart,name='increment_cart'),
    path('remove_cart/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('handle-color-selection/', views.handle_color_selection, name='color_selection'),

    path('checkout',views.checkout,name='checkout'),

    path('wishlist',views.wishlist,name='wishlist'),
    path('add_wishlist/<int:product_id>/',views.add_wishlist,name='add_wishlist'),
    path('delete_wishlist/<int:wishlit_item_id>/',views.delete_wishlist,name='delete_wishlist'),

    path('add_address_checkout/<int:user_id>/',views.add_address_checkout,name='add_address_checkout'),

    


]
