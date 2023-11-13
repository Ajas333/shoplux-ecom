from django import forms
from .models import Product,Product_Variant

class CreateProductForm(forms.ModelForm):
    
            
    class Meta:
        model = Product
        fields =['product_name','product_catg','sku_id','product_brand','max_price','sale_price','product_description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

# class AddVeriantForm(forms.ModelForm):

#     class Meta:
#         model = Product_Variant
#         fields =['product','atributes','stock']

#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
        
       