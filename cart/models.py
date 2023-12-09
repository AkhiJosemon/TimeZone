from django.db import models
from baseapp.models import *
from category.models import Product
from category.models import Variant






# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
    def is_product_in_cart(self, product):
        # Check if the product is in the cart items
        return self.cartitem_set.filter(product=product).exists()

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations =  models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    

    def sub_total(self):
        return self.product.price * self.quantity
    
    def update_quantity(self, new_quantity):
        self.quantity = new_quantity
        self.save()

    
    
    def __str__(self):
        return self.product.product_name    
    
    def get_sub_total(self):
        return self.product.get_final_price() * self.quantity

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations =  models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Wishlist for {self.user.username}"
