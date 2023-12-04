from django import forms
from .models import ProductOffer

class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields = ['title', 'product','end_date', 'discount','image']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            
        }