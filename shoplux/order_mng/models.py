from django.db import models
from user_log.models import Account,Address
from product_det.models import Product_Variant

# Create your models here.

class Payment(models.Model):
    user=models.ForeignKey(Account, on_delete=models.CASCADE)
    Payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount_paid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Payment_id


class Order(models.Model):
    STATUS=(
        ('New','New'),
        ('Acceepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),

    )
    user=models.ForeignKey(Account, on_delete=models. CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL, null=True)
    order_id=models.CharField(max_length=100)
    address=models.ForeignKey(Address, on_delete=models.CASCADE)
    order_note=models.CharField(max_length=100, blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    ip=models.CharField(blank=True, max_length=20)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username


class OrderProduct(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    Payment=models.ForeignKey(Payment,on_delete=models.SET_NULL, blank=True, null=True)
    user=models.ForeignKey(Account, on_delete=models.CASCADE)
    product_variant=models.ForeignKey(Product_Variant, on_delete=models.CASCADE)
    color=models.CharField(max_length=30)
    size=models.CharField(max_length=30)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)
    
    def sub_total(self):
        return self.product_variant.product.sale_price * self.quantity
    
    def __str__(self):
        return self.product_variant.product_variant_slug