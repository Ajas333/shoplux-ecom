from django.contrib import admin
from .models import Cart,CartItem,Wishlist,WishlistItems
# Register your models here.

class WishlistUserAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Note the comma after 'user' to create a tuple
    search_fields = ('user',)

class WishlistUserItemsAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product')
    search_fields = ('wishlist',)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist, WishlistUserAdmin)
admin.site.register(WishlistItems, WishlistUserItemsAdmin)

