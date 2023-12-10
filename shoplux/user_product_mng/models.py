from django.db import models
from product_det.models import Product,Product_Variant,Atribute_Value
from user_log.models import Account
from django.shortcuts import get_object_or_404
from Coupon_Mng.models import Coupon

# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=250, blank=True)
    date_added=models.DateField(auto_now_add=True)
    coupen=models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product_variant=models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)
    color = models.ForeignKey(Atribute_Value, related_name='cart_color', on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Atribute_Value, related_name='cart_size', on_delete=models.SET_NULL, null=True)

    def sub_total(self):
        if self.product_variant.product.product_offer is not None and self.product_variant.product.product_offer > 0:
            return self.product_variant.product.product_offer * self.quantity
        else:  
            return self.product_variant.product.sale_price * self.quantity
    
class Wishlist(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE)


class WishlistItems(models.Model):
    wishlist=models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)

    


