from django import forms


class AddToCartForm(forms.Form):
    qty = forms.DecimalField(min_value=1, decimal_places=0)
