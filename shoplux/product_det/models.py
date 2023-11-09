from django.db import models
from django.utils.text import slugify
from django.db.models import UniqueConstraint, Q,F,Avg,Count
from collections import defaultdict
from django.urls import reverse
from datetime import datetime
    # Create your models here.


class Category(models.Model):
        category_name = models.CharField(max_length=20, unique=True)
        slug = models.SlugField(max_length=20, unique=False)
        description = models.TextField(max_length=200, blank=True)
        parent = models.ForeignKey('self',null=True, blank=True, on_delete=models.CASCADE)
        is_available = models.BooleanField(default=True)
        
        

        class Meta:
            verbose_name = 'category'
            verbose_name_plural = 'categories'

        def save(self, *args, **kwargs):
            self.slug = slugify(self.category_name)
            super(Category, self).save(*args, **kwargs)

        def __str__(self):
            return self.category_name
        


class Brand(models.Model):
        brand_name = models.CharField(max_length=50,unique=True)
        is_active = models.BooleanField(default=True)

        def __str__(self):
            return self.brand_name
        

class Atribute(models.Model):
        atribute_name = models.CharField(max_length=50,unique=True)
        is_active = models.BooleanField(default=True)

        def __str__(self):
            return self.atribute_name
        

class Atribute_Value(models.Model):
        atribute = models.ForeignKey(Atribute,on_delete=models.CASCADE)
        atribute_value = models.CharField(max_length=50,unique=True)
        is_active = models.BooleanField(default=True)

        def __str__(self):
            return self.atribute_value+"-"+self.atribute.atribute_name
        

class Product(models.Model):
        product_name = models.CharField(max_length=100)
        product_catg = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
        sku_id = models.CharField(max_length=30)
        product_brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
        max_price = models.DecimalField(max_digits=8, decimal_places=2)
        sale_price = models.DecimalField(max_digits=8, decimal_places=2)
        product_slug = models.SlugField(unique=True, blank=True,max_length=200)
        product_description = models.TextField(max_length=250)
        image = models.ImageField(upload_to='static/image_admin/items')
        is_active = models.BooleanField(default=True)
        created_at =models.DateTimeField(auto_now_add=True)
        updated_at =models.DateTimeField(auto_now=True)
        

        def save(self, *args, **kwargs):
            product_slug_name = f'{self.product_brand.brand_name} {self.product_name} {self.sku_id} {self.product_catg.category_name}'
            base_slug = slugify(product_slug_name)
            counter = Product.objects.filter(product_slug__startswith=base_slug).count()
            if counter > 0:
                self.product_slug = f'{base_slug}-{counter}'
            else:
                self.product_slug = base_slug
            super(Product, self).save(*args, **kwargs)


        def __str__(self):
            return self.product_brand.brand_name+"-"+self.product_name+"-"+self.product_catg.category_name
        



class Product_Variant(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE)
        atributes = models.ManyToManyField(Atribute_Value,related_name='attributes')
        stock = models.IntegerField()
        product_variant_slug = models.SlugField(unique=True, blank=True,max_length=200)
        thumbnail_image = models.ImageField(upload_to='static/image_admin/items')
        is_active = models.BooleanField(default=True)
        created_at =models.DateTimeField(auto_now_add=True)
        updated_at =models.DateTimeField(auto_now=True)

        def save(self, *args, **kwargs):
            product_variant_slug_name = f'{self.product.product_brand.brand_name}-{self.product.product_name}-{self.product.product_catg.category_name}'
            base_slug = slugify(product_variant_slug_name)
            counter = Product_Variant.objects.filter(product_variant_slug__startswith=base_slug).count()
            if counter > 0:
                self.product_variant_slug = f'{base_slug}-{counter}'
            else:
                self.product_variant_slug = base_slug
            super(Product_Variant, self).save(*args, **kwargs)

 
        
        