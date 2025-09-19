
from django import forms

# Form used during the checkout process to collect shipping and payment information
class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)

    card_number = forms.CharField(max_length=19, label="Card Number")
    card_expiry = forms.CharField(max_length=5, label="Expiry (MM/YY)")
    card_cvc = forms.CharField(max_length=4, label="CVC")