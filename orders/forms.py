from django import forms



class CartFrom(forms.Form):
    quantity = forms.IntegerField(min_value=1,max_value=9)