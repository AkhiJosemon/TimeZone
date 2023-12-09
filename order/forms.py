from django import forms
from .models import *

class PaymentMethodForm(forms.Form):
    payment_method = forms.CharField(max_length=100)
 