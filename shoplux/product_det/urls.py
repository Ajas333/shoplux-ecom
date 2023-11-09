from django.urls import path
from product_det import views

app_name = 'product_details'


urlpatterns = [
    path('product_list',views.product_list,name='product_list'),
    path('add_product',views.add_product,name='add_product'),
    path('product_det/<int:product_id>/',views.product_det,name='product_det'),
    path('update_product/<int:product_id>/',views.update_product,name='update_product'),
  



    path('category',views.category,name='category'),
    path('add_category',views.add_category,name='add_category'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),
    path('available/<int:category_id>/',views.available,name='available'),
    path('edit_category/<int:category_id>/',views.edit_category,name='edit_category'),



    path('add_brand',views.add_brand,name='add_brand'),
    path('brand_available/<int:brand_id>/',views.brand_available,name='brand_available'),
    path('brand',views.brand,name='brand'),
    path('delete_brand/<int:brand_id>/',views.delete_brand,name='delete_brand'),



    path('attribute',views.attribute,name='attribute'),
    path('add_attribute',views.add_attribute,name='add_attribute'),
    path('attribute_available/<int:attribute_id>/',views.attribute_available,name='attribute_available'),
    path('delete_attribute/<int:attribute_id>/',views.delete_attribute,name='delete_attribute'),



    path('attribute_value',views.attribute_value,name='attribute_value'),
    path('add_attribute_value',views.add_attribute_value,name='add_attribute_value'),
    path('attribute_value_available/<int:attribute_value_id>/',views.attribute_value_available,name='attribute_value_available'),
    path('delete_attribute_value/<int:attribute_value_id>/',views.delete_attribute_value,name='delete_attribute_value'),

]                                  