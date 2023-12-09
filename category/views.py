from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from  category.models import *
from  baseapp.models import Account
from .models import Category,Product
from django.contrib.auth import authenticate,login,logout
from .forms import *
from order.models import *
from django.http import HttpResponseBadRequest
# Create your views here
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from .models import Product, Variant
from .forms import VariantForm

def catagory_list(request):
    categories = Category.objects.all()
    sub_categories=SubCategory.objects.all()
    context={

        'categories': categories,
        'sub_categories':sub_categories
    }

    return render(request,'admin/catogry.html',context)



def add_catagory(request):
    return render(request,'admin/add_catagory.html')

def sub_add_catagory(request):
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render (request,'admin/sub_add_catagory.html',context)

def insert_catagoriy(request):
    if request.method =="POST":
       catagory_name= request.POST.get("catagory_name")
    
       description= request.POST.get("description")

       print(catagory_name,description)
       dn= Category(category_name=catagory_name,description= description )
       dn.save()
       print('123')
       return redirect("category:add_catogory")


def insert_sub_catagoriy(request):
    if request.method =="POST":
        sub_catagory_name= request.POST.get("sub_catagory_name")
        category_id = request.POST.get("category")
        print(category_id)
        category=Category.objects.get(pk=category_id)
        print(category)
    
       
        dn= SubCategory(subcategory_name=sub_catagory_name,category=category)
        dn.save()
        print('123')
        return redirect("category:sub_add_catogory")
   
def delete_category(request, slug):
    if request.method == 'POST':
        category = Category.objects.get(slug=slug)
        category.delete()
    return redirect('category:catogory_list')  # Redirect to the desired page after deletion

def sub_delete_category(request, slug):
    if request.method == 'POST':
        category = SubCategory.objects.get(slug=slug)
        category.delete()
    return redirect('category:catogory_list')  # Redirect to the desired page after deletion




def edit_catagory(request, category_name):
    category = get_object_or_404(Category, category_name=category_name)

    if request.method == "POST":
        catagory_name = request.POST.get("catagory_name")
        description = request.POST.get("description")

        category.category_name = catagory_name
        category.description = description
        category.save()
        print()
        return redirect('category:catogory_list')

    context = {'category': category}
    return render(request, 'admin/some.html', context)   

@login_required(login_url='baseapp:admin_pannel')
def sub_edit_catagory(request, category_name):
    category = get_object_or_404(SubCategory, subcategory_name=category_name)

    if request.method == "POST":
        catagory_name = request.POST.get("catagory_name")
        

        category.subcategory_name = catagory_name
        
        category.save()
        print()
        return redirect('category:catogory_list')

    context = {'category': category}
    return render(request, 'admin/some.html', context)   

@login_required(login_url='baseapp:admin_pannel')
def add_product(request):

    categories = Category.objects.all()
    sub_categories = SubCategory.objects.all()
    brands=Brand.objects.all()
    variant=Variant.objects.all()
    
    print(variant)
             
    if request.method == 'POST':
        brand_id = request.POST.get('brand')
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        sub_category_id=request.POST.get('sub_category')
        description = request.POST.get('description')
        price = request.POST.get('price')        
        product_id = request.POST.get('product_id')
        images = request.FILES.getlist('images[]')
        brand_id = request.POST.get('brand')
        brand = Brand.objects.get(id=brand_id) 
        category = Category.objects.get(pk=category_id)
        sub_category=SubCategory.objects.get(pk=sub_category_id)
        cropped_image_data = request.POST.get('cropped_image')
        
        if  not product_name or not category_id or not sub_category_id or not description or not price or not images:
            messages.error(request, 'All fields must be filled.')
            return redirect('category:add_product')

        # Check if price is a positive integer
        if not price.isdigit():
            messages.error(request, 'Price must be a valid number.')
            return redirect('category:add_product')

        # Convert the price to an integer
        try:
            price = int(price)
            if price <= 0:
                raise ValueError()
        except ValueError:
            messages.error(request, 'Price must be a positive integer.')
            return redirect('category:add_product')


            
        product = Product(brand=brand,product_name=product_name, description=description,category=category,subcategory=sub_category, price=price, rprice=price)
        product.image=images[0]#cropped_image_data#images[0]
        product.save()
        
        for i in range(len(images)):
            prd_image = ProductImage(product=product, image=images[i])
            prd_image.save()

        return redirect('category:product_list')
    else:

        form=AddProductForm()

    context = {
           'form': form,
           'categories': categories,
           'brands':brands,
           'variants': variant,
           'sub_categories':sub_categories
         }      
        
   
        

    return render(request,'admin/add_product.html',context)



def delete_product(request,product_id):

    if request.method== 'POST':
         
        product=Product.objects.get(product_id=product_id)
        product.is_active = False
        product.save()

    return redirect('category:product_list')     
  


@login_required(login_url='baseapp:admin_pannel')
def edit_product(request, product_id):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # Retrieve the product to be edited
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # Handle the case where the product doesn't exist
        return HttpResponse("Product not found", status=404)

    if request.method == 'POST':
        # Update the product with the form data
        product.product_name = request.POST.get('product_name')
        product.category = Category.objects.get(pk=request.POST.get('category'))
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.brand = Brand.objects.get(pk=request.POST.get('brand'))
        product.stocks = request.POST.get('stock')

        # Handle image updates (if needed)
        new_images = request.FILES.getlist('images[]')
        if new_images:
            # Clear existing product images and add new ones
            ProductImage.objects.filter(product=product).delete()
            for image in new_images:
                prd_image = ProductImage(product=product, image=image)
                prd_image.save()

        # Save the updated product
        product.save()

        return redirect('category:product_list')
    else:
        # Populate the form with existing product data
        form = AddProductForm(instance=product)

    context = {
        'form': form,
        'categories': categories,
        'brands': brands,
        'product': product,  # Include the product object in the context for reference
    }  
    return render(request, 'admin/edit_product.html', context)





        



@login_required(login_url='baseapp:admin_pannel')
def produ(request):
    if request.user.is_authenticated and not request.user.is_authenticated:
        if not request.user.is_superadmin:
            return redirect('baseapp:admin_pannel')
        
    
    search_query = request.GET.get('search', '')

    # Query the products baseappd on the search query and exclude soft-deleted products
    if search_query:
        products = Product.objects.filter(product_name__icontains=search_query, is_active=True)
    else:
        products = Product.objects.filter(is_active=True)

    context = {
        'products': products
    }

    # Provide the correct template name 'admin/product.html'
    return render(request, 'admin/products.html', context)


@login_required(login_url='baseapp:admin_pannel')
def pro(request):
   
   return render(request,'admin/product.html' )


def user_list(request):
    users =  Account.objects.exclude(is_superadmin=True)
    
    context={
        'users':users
    }
    return render(request,'admin/user.html',context)


def action_user(request,user_id):
    
    user = get_object_or_404(Account, id=user_id)



    # Toggle the is_blocked status of the user
    if user.is_active:
        user.is_active=False
        if request.user == user:
            logout(request)

    else:
        user.is_active=True
        
    user.save()
    return redirect('category:user_list')


    


@login_required(login_url='baseapp:admin_pannel')
def product_list(request):
    product= Product.objects.all()

    return render('admin/')

@login_required(login_url='baseapp:admin_pannel')
def brand(request):
    return render(request,'admin/page-brands.html')

@login_required(login_url='baseapp:admin_pannel')
def insert_brand(request):
    if request.method == "POST":
        brand_name = request.POST.get("Brand_name")
        print(brand_name)
        dn = Brand(brand_name=brand_name)
        dn.save()
        print('123')
        return redirect("category:add_brand")
    return render(request,'admin/addbrand.html') 
    
    
def delete_brand(request, slug):
    if request.method == 'POST':
        brand = Brand.objects.get(slug=slug)
        brand.delete()
    return redirect('category:brand_list')  # Redirect to the desired page after deletion

@login_required(login_url='baseapp:admin_pannel')
def brand_list(request):
    brand = Brand.objects.all()

    context={

        'brand': brand
    }

    return render(request,'admin/listbrand.html',context)







@login_required(login_url='baseapp:admin_pannel')
def add_variant(request):
    

    form=VariantForm(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        return redirect('category:variant_list')
    else:
        messages.error(request,'Invalid Data')

    


    return render(request, 'admin/addvariants.html', {'form': form})
    
    
    
    
@login_required(login_url='baseapp:admin_pannel')   
def variant_list(request):
    product_variations = Variant.objects.all()

    context = {'product_varient': product_variations}
    return render(request, 'admin/listvariants.html', context)

@login_required(login_url='baseapp:admin_pannel   ')
def brand_list(request):
    brand = Brand.objects.all()

    context={

        'brand': brand
    }

    return render(request,'admin/listbrand.html',context)

@login_required(login_url='baseapp:admin_pannel')
def Order_list(request):
    orders = Order.objects.all()
    
    context = {
        'orders': orders,
        
    }
    
    return render(request,'ADMIN/order.html',context)

@login_required(login_url='baseapp:admin_pannel')
def update_order_status(request,order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=int(order_id))
        status = request.POST['status']
        if status=='Cancelled':
            user_profile = request.user
            wallets,create = Wallet.objects.get_or_create(user=user_profile)

        # Credit the purchased amount back to the wallet
            wallets.wallet_amount += order.order_total
            wallets.wallet_amount = round(wallets.wallet_amount, 2)
            wallets.save()
        order.status = status
        order.save()
        return redirect('category:Order_list')
    else:
        return HttpResponseBadRequest("Bad request.")

@login_required(login_url='baseapp:admin_pannel')    
def edit_variant(request,var_id):
    variant = get_object_or_404(Variant, pk=var_id)

    if request.method == 'POST':
        form = VariantForm(request.POST, instance=variant)
        if form.is_valid():
            form.save()
            return redirect('category:variant_list')
    else:
        form = VariantForm(instance=variant)

    context = {
        'form': form,
        'variant': variant,
    }
    return render(request, 'ADMIN/editvarients.html', context)


def delete_variant(request,var_id):
    if request.method=='POST':
        variant = get_object_or_404(Variant, pk=var_id)
        variant.delete()
    return redirect('category:variant_list')

@login_required(login_url='baseapp:admin_pannel')
def coupons_list(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons': coupons
    }
    return render(request, 'ADMIN/couponslist.html', context)

@login_required(login_url='baseapp:admin_pannel')
def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category:coupons_list')  # Redirect to a page displaying the list of coupons
    else:
        form = CouponForm()

    return render(request, 'ADMIN/addcoupons.html', {'form': form})

def delete_coupon(request,coup_id):
    if request.method=='POST':
        coupon = get_object_or_404(Coupon, pk=coup_id)
        coupon.delete()
    return redirect('category:coupons_list')

@login_required(login_url='baseapp:admin_pannel')
def edit_coupon(request,coup_id):
    coupon = get_object_or_404(Coupon, pk=coup_id)

    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('category:coupons_list')
    else:
        form = CouponForm(instance=coupon)

    context = {
        'form': form,
        'coupon':coupon,
    }
    return render(request, 'ADMIN/editcoupons.html', context)


def add_product_offer(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = ProductOfferForm(request.POST)
        if form.is_valid():
            offer = form.save()
            product.offers.add(offer)
            return redirect('category:productofferlist')
    else:
        form = ProductOfferForm()

    return render(request, 'Admin/add_product_offer.html', {'form': form, 'product': product})

@login_required(login_url='baseapp:admin_pannel')
def add_category_offer(request, category_id):
    category = Category.objects.get(pk=category_id)

    if request.method == 'POST':
        form = CategoryOfferForm(request.POST)
        if form.is_valid():
            offer = form.save()
            category.offers.add(offer)
            return redirect('category:productofferlist')
    else:
        form = CategoryOfferForm()

    return render(request, 'ADMIN/add_category_offer.html', {'form': form, 'category': category})

@login_required(login_url='baseapp:admin_pannel')
def productofferpage(request):
    product=Product.objects.all()
    context={
        'products' : product
    }
    return render(request,'ADMIN/select_product.html',context)

@login_required(login_url='baseapp:admin_pannel')
def categoryofferpage(request):
    category=Category.objects.all()
    context={
        'category' : category
    }
    return render(request,'ADMIN/select_category.html',context)

@login_required(login_url='baseapp:admin_pannel')
def productofferlist(request):
    offer=Offer.objects.all()
    context={
        'offer' : offer
    }
    return render(request,'ADMIN/productofferlist.html',context)


def categoryofferlist(request):
    return redirect('category:productofferlist')

def delete_productoffer(request,off_id):
    offer=Offer.objects.get(pk=off_id)
    offer.delete()
    return redirect('category:productofferlist')