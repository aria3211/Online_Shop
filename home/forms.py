from django import forms
from .models import Product,Category



class PhotoForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image']
    def clean_price(self):
        price = self.cleaned_data['price']
        if not price:
            price = 0  # or any default value
        return price
    