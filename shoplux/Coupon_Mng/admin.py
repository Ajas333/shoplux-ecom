from django.contrib import admin

from .models import Coupon

class CouponAdmin(admin.ModelAdmin):
    list_display = ('coupon_id', 'start_date', 'end_date', 'discount_rate','is_active')
    search_fields = ('coupon_id',)

admin.site.register(Coupon, CouponAdmin)
