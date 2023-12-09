from django.db import models
from django.utils import timezone
from baseapp.models import *
from category.models import *
from cart.models import *
from datetime import timedelta

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _str_(self):
        return self.payment_id
    
    
class Order(models.Model):
    STATUS =(
        ('New','New'),
        ('Accepted','Accepted'),
        ('Delivered','Delivered'),
        ('Cancelled','Cancelled'),
        ('Rejected','Rejected'),
        ('Returned','Returned'),
    )
    user=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=20)
    order_total = models.FloatField(null=True, blank=True)
    tax=models.FloatField(null=True)
    status=models.CharField(max_length=10, choices=STATUS, default='New')
    ip =  models.CharField(blank=True,max_length=20)
    is_ordered=models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now,)
    updated_at=models.DateTimeField(default=timezone.now,)
    selected_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    discount=models.FloatField(null=True)
    paymenttype=models.CharField(max_length=100,null=True)
    
    def _str_(self):
        return self.user.first_name
    
class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    #product_type=models.CharField(max_length=20)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    #color = models.CharField(max_length=50,null=True)
    #size = models.CharField(max_length=50,null=True)
    variations =  models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    

    def _str_(self):
        return self.product.product_name
    


class Wallet(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    wallet_amount = models.FloatField(default=0)
    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}, {self.wallet_amount}"
    
class Coupon(models.Model):
    coupon_name = models.CharField(max_length=255, unique=True)
    minimum_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    maximum_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_amount = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(blank=True, default=timezone.now() + timedelta(days=365))  # Default expiration date is one year from now
   
    
    def __str__(self):
        return self.coupon_name
    
class Redeemed_Coupon(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    redeemed_date = models.DateTimeField(auto_now_add=True)
   