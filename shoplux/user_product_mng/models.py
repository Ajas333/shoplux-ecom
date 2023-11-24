from django.db import models
from product_det.models import Product,Product_Variant,Atribute_Value
from django.shortcuts import get_object_or_404

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250, blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product_variant=models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    color = models.ForeignKey(Atribute_Value, related_name='cart_color', on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Atribute_Value, related_name='cart_size', on_delete=models.SET_NULL, null=True)

    def sub_total(self):
        return self.product_variant.product.sale_price * self.quantity
    


    


