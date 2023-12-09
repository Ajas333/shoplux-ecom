from django.contrib import admin
from .models import Payment,Order,OrderProduct
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'order_total', 'status','coupen')
    search_fields = ('order_id',)

admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)


