from django import forms
from user_log.models import Address
from .models import Address



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['house_name', 'streat_name', 'post_office', 'place', 'district', 'state', 'country', 'pincode']