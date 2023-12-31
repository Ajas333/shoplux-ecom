# from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings 



class AccountManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not email:
            raise ValueError("User must have a email")
        if not username:
            raise ValueError("User must have an username")
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            
        )

        # user.is_active = True
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Custom user model
class Account(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=254, unique=True)
    phone=models.CharField(null=False, blank=False)
    image = models.ImageField(upload_to='static/image_admin/people', blank=True, null=True)
    

   
    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManager()

    def __str__(self):
        return self.email

    # Check user permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Check user module permissions
    def has_module_perms(self, add_label):
        return True

class Address(models.Model):
    account=models.ForeignKey(Account,on_delete=models.CASCADE)
    house_name=models.CharField(max_length=40,null=False, blank=False)
    streat_name=models.CharField(max_length=50,null=False, blank=False)
    post_office=models.CharField( max_length=20,null=False, blank=False)
    place=models.CharField(max_length=25,null=False, blank=False)
    district=models.CharField(max_length=20, null=False, blank=False)
    state=models.CharField(max_length=30,null=False,blank=False)
    country=models.CharField(max_length=35,null=True,blank=True)
    pincode=models.CharField(max_length=10,null=True, blank=True)
    is_default = models.BooleanField(default=False)

    

class Wallet(models.Model):
    user=models.OneToOneField(Account, on_delete=models.CASCADE)
    balance=models.IntegerField(default=0)
    
class WalletHistory(models.Model):
    wallet=models.ForeignKey(Wallet, on_delete=models.CASCADE)
    type=models.CharField(null=True, blank=True, max_length=20)
    created_at=models.DateField(auto_now_add=True)
    amount=models.IntegerField()

