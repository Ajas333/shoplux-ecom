from .models import Cart,CartItem,Wishlist,WishlistItems
from .views import _cart_id


def counter(request):
    cart_count = 0
    wishlist_count = 0

    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))

            if request.user.is_authenticated:  # Check if the user is authenticated
                wishlist = Wishlist.objects.filter(user=request.user).first()
                if wishlist:
                    wishlist_items = WishlistItems.objects.filter(wishlist=wishlist)
                    wishlist_count = wishlist_items.count()

                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart_items = CartItem.objects.filter(cart=cart[:1])

            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0

    return {'cart_count': cart_count, 'wishlist_count': wishlist_count}