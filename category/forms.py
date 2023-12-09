from category.models import Product
from baseapp.models import Address
from  django import forms
from .models import *
from order.models import *
from decimal import Decimal 
from django.core.exceptions import ValidationError

class AddProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [ 'product_name','brand', 'category'
                  , 'description', 'price', 'image']


    def clean(self):
        cleaned_data = super().clean()
        stocks = cleaned_data.get('stocks')
        price = cleaned_data.get('price')

        # Check if stocks or price is less than zero
        if stocks is not None and stocks < 0:
            raise forms.ValidationError("Stock cannot be a negative value.")

        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be a negative value.")
        
        
        
class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = ['color', 'body_type', 'strap_type', 'stocks', 'product']

    def clean(self):
        cleaned_data = super().clean()
        color = cleaned_data.get('color')
        body_type = cleaned_data.get('body_type')
        strap_type = cleaned_data.get('strap_type')
        product = cleaned_data.get('product')

        # Check if a variant with the same combination already exists
        if Variant.objects.filter(color=color, body_type=body_type, strap_type=strap_type, product=product).exists():
            raise ValidationError('A variant with the same combination already exists.')

        return cleaned_data
        
class DateInput(forms.DateInput):
    input_type = 'date'

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_name', 'minimum_purchase', 'maximum_purchase', 'coupon_amount', 'expiry_date']
        widgets = {
            'expiry_date': DateInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values for the new fields
        self.fields['expiry_date'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
        self.fields['expiry_date'].initial = timezone.now() + timedelta(days=365)
        
        instance = kwargs.get('instance')
        if instance:
            self.fields['coupon_name'].initial = instance.coupon_name
            self.fields['minimum_purchase'].initial = instance.minimum_purchase
            self.fields['maximum_purchase'].initial = instance.maximum_purchase
            self.fields['coupon_amount'].initial = instance.coupon_amount
            self.fields['expiry_date'].initial = instance.expiry_date
           
    def clean_expiry_date(self):
        expiry_date = self.cleaned_data['expiry_date']
        if expiry_date and expiry_date < timezone.now().date():
            raise forms.ValidationError("Expiration date must be in the future.")
        return expiry_date

    def clean(self):
        cleaned_data = super().clean()
        minimum_purchase = cleaned_data.get('minimum_purchase')
        coupon_amount = cleaned_data.get('coupon_amount')

        if minimum_purchase is not None and coupon_amount is not None and coupon_amount >= Decimal('0.15') * minimum_purchase:
            raise forms.ValidationError("Coupon amount must be less than 15% of the minimum purchase.")

        return cleaned_data
    
    
    
class ProductOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['name', 'discount_percentage', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']

        # Ensure the discount percentage is less than or equal to 70%
        max_allowed_discount = Decimal('70')
        if discount_percentage > max_allowed_discount:
            raise forms.ValidationError("Discount percentage cannot be greater than 70%.")

        return discount_percentage
    
    
class CategoryOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['name', 'discount_percentage', 'start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
    
    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data['discount_percentage']

        # Ensure the discount percentage is less than or equal to 70%
        max_allowed_discount = Decimal('15')
        if discount_percentage > max_allowed_discount:
            raise forms.ValidationError("Discount percentage cannot be greater than 70%.")

        return discount_percentage