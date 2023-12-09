from django.shortcuts import render,HttpResponse,redirect,get_object_or_404 
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import *
from category.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache 
from django.contrib.sessions.models import Session
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cart.models import*
from django.core.exceptions import ObjectDoesNotExist
from order.models import *
import random
from django.contrib import auth

@never_cache
def index(request):
    return render(request,'USER/index.html')
    

@never_cache
def handlelogin(request):
    
    if request.user.is_authenticated:
        return redirect('baseapp:index')
    
    
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)

        if not Account.objects.filter(email=email).exists():
            messages.error(request, "Invalid Email Adress")
            return redirect('baseapp:login')
        
        if not Account.objects.filter(email=email,is_active=True).exists():
            messages.error(request, "You are blocked by admin ! Please contact admin ")
            return redirect('baseapp:login') 
        
        user = authenticate(email=email,password=password)
        print(user)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('baseapp:login')
        else:
            login(request,user)
            messages.success(request, "Login successful!")
            return redirect('baseapp:index')
            
    return render(request,'USER/login.html')


@never_cache
def signup(request):
    if request.user.is_authenticated:
        return redirect('baseapp:index')
    
    if request.method == 'POST':
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("password1")
        referral_code = request.POST.get("referral_code")

        # Validate referral code
        referred_by = None
        if referral_code:
            try:
                referred_by = Account.objects.get(referral_code=referral_code)
            except Account.DoesNotExist:
                messages.error(request, "Invalid referral code")
                return redirect('baseapp:signup')

        if Account.objects.filter(email=email).exists():
            messages.error(request, "Existing Email Address")
            return redirect('baseapp:signup')
        
        if pass1 != pass2:
            messages.error(request, "Mismatch in password")
            return redirect('baseapp:signup')
        
        # Create the user
        user = Account.objects.create_user(email=email, password=pass1, username=username, first_name=first_name, last_name=last_name)
        
        # Add referral bonus to wallets
        if referred_by:
            referred_by_wallet, created = Wallet.objects.get_or_create(user=referred_by)
            referred_by_wallet.wallet_amount += 100
            referred_by_wallet.save()

            user_wallet, created = Wallet.objects.get_or_create(user=user)
            user_wallet.wallet_amount += 100
            user_wallet.save()

        request.session['email'] = email
        return redirect('baseapp:sp')

    return render(request, "USER/signup.html")

@never_cache
def sent_otp(request):
    randomn=random.randint(1000,9999)
    request.session['otpn']=randomn

    send_mail(
     "OTP AUTHENTICATING TimeZone",
     f"{randomn} -OTP",
     "akhijosemon@gmail.com",
     [request.session['email']],
     fail_silently=False,
      )
    return redirect('baseapp:vp')

@never_cache
def verify_otp(request):
    user=Account.objects.get(email=request.session['email'])
    if request.method=="POST":
        if str(request.session['otpn'])!= str(request.POST['otp']):
            messages.error(request,"invalid otp")

        else:
            user.is_active=True
            user.save()
            login(request,user)
            messages.success(request, "signup successful!")
            return redirect('baseapp:index')
    return render(request,'user/otpverifypage.html')

def resend_otp(request):
    return redirect('baseapp:sp')
    
@never_cache
def products(request):
    products = Product.objects.filter(is_active=True, variant__isnull=False).distinct()

    if request.method == 'GET':
        # Get filter values from the request
        category = request.GET.get('category')
        brand = request.GET.get('brand')
        min_price = request.GET.get('min_price')
        if not min_price:
            min_price = 0  
        max_price = request.GET.get('max_price')
        if not max_price:
            max_price = 99999

        sort_by = request.GET.get('sort_by')

        if category:
            selected_category = Category.objects.get(pk=category)
        else:
            selected_category = 'All'
        if brand:
            selected_brand = Brand.objects.get(pk=brand)
        else:
            selected_brand = 'All'

        if category and brand:
            products = products.filter(category=category, brand=brand)
        elif category:
            products = products.filter(category=category)
        elif brand:
            products = products.filter(brand=brand)

        if max_price and min_price:
            products = products.filter(price__gte=min_price, price__lte=max_price)

        # Apply sorting
        if sort_by == 'highToLow':
            products = products.order_by('-price')
        elif sort_by == 'lowToHigh':
            products = products.order_by('price')

        categories = Category.objects.all()
        brands = Brand.objects.all()

        products_with_offer_price = []
        products_without_offer = []

        for product in products:
            offer_price = product.get_final_price()

            if offer_price != product.price:
                product.checkprice = offer_price
                product.dis_price = product.price

                product.save()
                products_with_offer_price.append(product)
            elif offer_price == product.price:
                products_without_offer.append(product)

        context = {
            'products': products_without_offer,
            'offered_products': products_with_offer_price,
            'selected_category': selected_category,
            'selected_brand': selected_brand,
            'selected_sort_by': sort_by,
            'categories': categories,
            'brands': brands,
            'min_price': min_price,
            'max_price': max_price,
        }

        return render(request, 'user/productlist.html', context)
    else:
        categories = Category.objects.all()
        brands = Brand.objects.all()
        context = {
            'products': products,
            'categories': categories,
            'brands': brands,
        }
        return render(request, 'USER/--', context)

@never_cache
def gotoproduct(request,product_id):
    products = Product.objects.get(pk=product_id)
    variants=Variant.objects.filter(product=products)
    product_category = products.category
    
    # Fetch three other products from the same category (excluding the selected product)
    related_products = Product.objects.filter(category=product_category).exclude(pk=products.pk)[:3]
    context= {
        'products' : products,
        'variants': variants,
        'related_products': related_products
     }

    return render(request, 'USER/page.html', context)

@never_cache
def user_logout(request):
    logout(request)
    messages.success(request, "logout successful!")
    return redirect('baseapp:index')

@never_cache
def base(request):
    print("hi")
    return redirect('order:admin_dashboard')
    
@never_cache
def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superadmin:
            return redirect('order:admin_dashboard')
    
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        print(email,password)
        user = authenticate(email=email, password=password)
        if user:
            if user.is_superadmin:
                login(request, user)
                messages.success(request, "Admin login successful!")
                print("hello")
                return redirect('baseapp:base')  # Use the named URL pattern
            messages.error(request, "Invalid admin credentials!")
    return render(request, 'ADMIN/login.html')

@never_cache
def admin_logout(request):
    logout(request)
    return redirect('baseapp:admin_pannel')



#base page
@never_cache
def db(request):
    if not request.user.is_authenticated:
        if not request.user.is_superadmin:
            return redirect('baseapp:admin_pannel')

    return render(request,'admin/inheritance.html')
#product click

@never_cache
def product_detail(request,product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        # Handle the case where the product doesn't exist
        return HttpResponse("Product not found", status=404)
    context= {
        'products':product
     }
    return render(request,'user/product.html',context)

# @never_cache
# def product_info(request):
#     return render(request,'user/product.html')

@never_cache
def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('baseapp:login')
    else:
        current_user = request.user
        data = Account.objects.filter(email=current_user.email).exclude(username='admin')
    
        context={
        'datas' : data
        }

        return render(request,'user/userprofile.html',context)

@login_required(login_url='baseapp:login') # Ensure the user is logged in
def mycart(request, total=0, quantity=0, cart_items=None):
    # Clear cart items for inactive products
    CartItem.objects.filter(user=request.user, product__is_active=False).delete()

    
    addresses = Address.objects.filter(user=request.user)
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, product__is_active=True, is_active=True)
            
            sub_total=[]    
            for cart_item in cart_items:
                pr=cart_item.product.get_final_price()
                sub_total.append(pr*cart_item.quantity)
            for cart_item in cart_items:
                pr=cart_item.product.get_final_price()
                sub_total.append(pr*cart_item.quantity)
                total += (pr* cart_item.quantity)
                quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total+tax
    except ObjectDoesNotExist:
        pass 

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'addresses' : addresses,
        'cart_items': cart_items,
        'sub_total':sub_total
    }

    return render(request, 'user/cart.html', context)
    

    


def manageaddress(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    
    context = {
        'addresses': addresses,
    }
    
    return render(request, 'user/manageadress.html', context)
    

def addaddress(request):
    
    if request.method == 'POST':
        user = request.user
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        postal_code = request.POST.get("postal_code")
        country = request.POST.get("country")
        phone_number = request.POST.get("phone_number")

        # Determine the address label
        addresses = Address.objects.filter(user=user)
        
      

        # Create the new address
        Address.objects.create(
            user=user,
            street=street,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            phone_number=phone_number,
        )
        

        return redirect('baseapp:manageaddress')

    return render(request, 'user/addadress.html')

def changepassword(request):
    if request.method=='POST':
        old_password=request.POST.get('old_password')
        new_password1=request.POST.get('new_password1')
        new_password2=request.POST.get('new_password2')
        user=request.user
        if not user.check_password(old_password):
            messages.error(request,'Old password is incorect')
        elif new_password1!=new_password2 :
           messages.error(request,'newpassword desnot match ')

        else:
            user.set_password(new_password1)
            user.save()
            auth.update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('baseapp:userprofile')  
    return render(request,'user/changepassword.html')
    

def showorder(request):
    orders = Order.objects.filter(user=request.user)

    context = {
        'orders': orders
    }
    return render(request,'user/showorder.html',context)

def coupons(request):
    return render(request,'user/coupons.html')


def edituserinfo(request):
        current_user = request.user
        data = Account.objects.get(email=current_user.email, username=current_user.username)

        if request.method == "POST":
            current_user.first_name = request.POST.get("first_name")
            current_user.last_name = request.POST.get("last_name")
            current_user.username = request.POST.get("username")
            current_user.save()
            return redirect('baseapp:userprofile')

        context = {
            'users': data
        }
        return render(request, 'user/edituserinfo.html', context)


def deleteadress(request,id):
    
    addresses = Address.objects.get(id=id)
    addresses.delete()
    return redirect('baseapp:manageaddress')


def set_default_address(request, address_id):
    user = request.user

    # Ensure that the address belongs to the user
    address = get_object_or_404(Address, id=address_id, user=user)

    # Set the selected address as default
    user.addresses.filter(is_default=True).update(is_default=False)
    address.is_default = True
    address.save()

    return redirect('baseapp:manageaddress')


def wallet(request):
    wallet_instance = None

    try:
        wallet_instance = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        pass

    return render(request, 'user/wallet.html', {'wallet': wallet_instance})

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('baseapp:login')
    else:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        return render(request, 'user/wishlist.html', {'wishlist_items': wishlist_items})
        
        
        
@login_required
def invite(request):
    # Assuming you have a Wallet model associated with the Account model
    referral_code = request.user.referral_code

    # You can customize the invite message as needed
    invite_message = f"Hey! Sign up on our website using my referral code: {referral_code}. Join now!"

    context = {
        'invite_message': invite_message,
        'invite_url': request.build_absolute_uri(reverse('baseapp:signup')),
    }

    return render(request, 'USER/invite.html', context)

def remove_wishlist(request,item_id):
    var=Wishlist.objects.get(pk=item_id)
    var.delete()
    return redirect('baseapp:wishlist')