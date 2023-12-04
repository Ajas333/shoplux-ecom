from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_catg', 'product_brand', 'max_price', 'sale_price', 'is_active')
    search_fields = ['product_name']

