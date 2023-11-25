from django.urls import path
from user_area import views

app_name = 'user_area'

urlpatterns = [
    path('user_profile/<int:user_id>/',views.user_profile,name='user_profile'),
    path('edit_user/<int:user_id>/',views.edit_user,name='edit_user'),
    path('change_password/<int:user_id>/',views.change_password,name='change_password'),
    path('logout',views.logout,name='logout'),
    path('add_address/<int:user_id>/',views.add_address,name='add_address'),
    path('set_default_address/<int:address_id>/',views.set_default_address,name='set_default_address'),
    path('edit_address/<address_id>/',views.edit_address,name='edit_address'),
    path('order_details/<int:order_id>/',views.order_details,name='order_details'),

]
