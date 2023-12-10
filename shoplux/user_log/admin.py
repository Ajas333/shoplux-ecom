from django.contrib import admin
from .models import Account,Wallet,WalletHistory


# Register your models here.
class UserWallet(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user',)
class UserWalletHistory(admin.ModelAdmin):
    list_display=('wallet','type','created_at','amount')
    search_fields=('Walet',)
admin.site.register(Account)
admin.site.register(Wallet,UserWallet)
admin.site.register(WalletHistory,UserWalletHistory)
