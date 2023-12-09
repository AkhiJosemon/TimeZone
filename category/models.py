from django.db import models
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.utils.text import slugify
from django.urls import reverse
from baseapp.models import *
from django.utils import timezone
from django.db import models
from django.utils.text import slugify
import uuid

# Create your models here.
class Offer(models.Model):
    name = models.CharField(max_length=100)
    discount_percentage = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description=models.TextField(max_length=250,blank=True)
    offers = models.ManyToManyField(Offer, related_name='categories', blank=True)
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def get_url(self):
        return reverse('user:product_by_category',args=[self.slug])

    def get_urls(self):
        return reverse('user:filter_product',args=[self.slug])    

    def __str__(self) -> str:
        return self.category_name




class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def save(self, *args, **kwargs):
        original_slug = slugify(self.subcategory_name)
        queryset = SubCategory.objects.filter(slug=original_slug)

        if queryset.exists():
            # If a SubCategory with the same slug exists, modify the slug
            suffix = 1
            while queryset.exists():
                modified_slug = f"{original_slug}-{suffix}"
                suffix += 1
                queryset = SubCategory.objects.filter(slug=modified_slug)
            
            self.slug = modified_slug
        else:
            self.slug = original_slug

        # Check uniqueness of subcategory_name
        original_name = self.subcategory_name
        name_queryset = SubCategory.objects.filter(subcategory_name=original_name)
        
        if name_queryset.exists():
            # If a SubCategory with the same name exists, modify the name
            name_suffix = 1
            while name_queryset.exists():
                modified_name = f"{original_name}-{name_suffix}"
                name_suffix += 1
                name_queryset = SubCategory.objects.filter(subcategory_name=modified_name)

            self.subcategory_name = modified_name
        
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.subcategory_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(unique=True, null=True, blank=True)


    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand_name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.brand_name
    


    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    offers = models.ManyToManyField(Offer, related_name='products', blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    checkprice=models.PositiveIntegerField(null=True)
    dis_price=models.PositiveIntegerField(null=True)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    rprice = models.IntegerField(null=True)
    temp=models.PositiveIntegerField(default=0)
    
    
   
        
    def __str__(self):
        return self.product_name
    
    
    def is_offer_valid(self, offer):
        today = timezone.now().date()
        return offer.start_date <= today <= offer.end_date

    def get_final_price(self):
        # Calculate the final price after applying the offer
        valid_product_offers = [offer for offer in self.offers.all() if self.is_offer_valid(offer)]
        valid_category_offers = [offer for offer in self.category.offers.all() if self.is_offer_valid(offer)]

        product_discount = max(offer.discount_percentage for offer in valid_product_offers) if valid_product_offers else 0
        category_discount = max(offer.discount_percentage for offer in valid_category_offers) if valid_category_offers else 0

        # Calculate the final price based on both product and category discounts
        final_discount = max(product_discount, category_discount)
        self.temp +=1
        return int(self.price * (100 - final_discount) / 100)
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    def __str__(self):
        if self.product:
            return f"Product: {self.product.brand}, {self.product.category}"
        else:
            return "Product: N/A"

class Variant(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    color = models.CharField(max_length=50,choices=[('black', 'Black'), ('silver', 'Silver'),('brown', 'brown'),('golden','Golden'),('blue','Blue'),('red','Red'),('green','Green')], blank=True)
    body_type = models.CharField(max_length=50, choices=[('resin', 'Resin'), ('metal', 'Metal')], blank=True)
    strap_type = models.CharField(max_length=50, choices=[('chain', 'Chain'), ('leather', 'Leather'), ('resin', 'Resin')], blank=True)
    stocks = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name = 'Variant'
        verbose_name_plural = 'Variants'

    def save(self, *args, **kwargs):
        unique_identifier = f"{self.color} {self.body_type} {self.strap_type} {uuid.uuid4()}"
        
        # Generate the slug using the combined fields
        self.slug = slugify(unique_identifier)
        super(Variant, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.color} {self.body_type} {self.strap_type}"   
    

 

            

    

    
    

    

    




