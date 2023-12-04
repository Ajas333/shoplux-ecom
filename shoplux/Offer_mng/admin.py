from django.contrib import admin
from .models import ProductOffer

@admin.register(ProductOffer)
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'start_date', 'end_date', 'discount', 'is_active')
    list_filter = ('start_date', 'end_date', 'is_active')
    search_fields = ['title']