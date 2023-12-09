from django.contrib import admin
from .models import Account,Wallet


# Register your models here.
class UserWallet(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user',)
admin.site.register(Account)
admin.site.register(Wallet,UserWallet)
