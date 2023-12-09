from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.http import HttpResponseBadRequest
from baseapp.models import *
from cart.models import *
from category.models import *
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from order.models import *
from django.views.decorators.cache import never_cache 

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


# Create your views here.
 # This decorator ensures the user is authenticated
def addtocart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('baseapp:login')
    else:
        product = Product.objects.get(product_id=product_id)



        variant = Variant.objects.get(product=product)



        if variant is not None:  # Check if variant was found
            stocks = variant.stocks

            if stocks > 0:
                if request.user.is_authenticated:
                    try:
                        is_cart_item_exists = CartItem.objects.filter(
                            user=request.user, product=product,
                            variations=variant).exists()
                        print(is_cart_item_exists)
                    except CartItem.DoesNotExist:
                        pass 

                    if is_cart_item_exists:
                        to_cart = CartItem.objects.get(user=request.user, product=product, variations=variant)
                        variation = to_cart.variations
                        if to_cart.quantity < variant.stocks:
                            to_cart.quantity += 1
                            to_cart.save()
                        else:
                            messages.success(request, "product out of stock")    
                    else:
                        cart = Cart.objects.create(cart_id=_cart_id(request))
                        to_cart = CartItem.objects.create(
                            user=request.user,
                            product=product,
                            variations=variant,  # Set the selected variation here
                            quantity=1,  # Set the initial quantity
                            is_active=True
                                                    )
                        # to_cart.variations.set([variant])  
                    return redirect('baseapp:mycart')
                else:
                    # try:
                    #     cart = Cart.objects.get(cart_id=_cart_id(request))
                    # except Cart.DoesNotExist:
                    #     cart = Cart.objects.create(cart_id=_cart_id(request))

                    # is_cart_item_exists = CartItem.objects.filter(cart=cart, product=product, variations=variant).exists()
                    # if is_cart_item_exists:
                    #     to_cart = CartItem.objects.get(cart=cart, product=product, variations=variant)
                    #     to_cart.quantity += 1
                    # else:
                    #     to_cart = CartItem(cart=cart, product=product, quantity=1)
                    # # to_cart.variations.set([variant])  # Use set() to manage the many-to-many relationship
                    # to_cart.save()
                    messages.success(request, "please login to purchase")
                    return redirect('baseapp:login')
            else:
                messages.warning(request, 'This item is out of stock.')
                return redirect('baseapp:gotoproduct', product_id)
        else:
            messages.warning(request, 'Variant not found.')  # Add an error message for debugging
            return redirect('baseapp:gotoproduct', product_id)

@never_cache  
def cartcheckout(request,total=0, quantity=0, cart_items=None):
    if not request.user.is_authenticated:
        return redirect('baseapp:login')
    
    try:
        tax = 0
        grand_total = 0
        coupon_discount = 0
        
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            adress=Address.objects.filter(user=request.user)
            
            #coupons = Coupon.objects.all()
        else:
            addresses = []


        for cart_item in cart_items:
            pr=cart_item.product.get_final_price()
            total += (pr * cart_item.quantity)
            quantity += cart_item.quantity

            try:
                
                if cart_item.variations.stocks <= 0:
                    print("Not enough stock!")
            except ObjectDoesNotExist:
                pass

        tax = (2 * total) / 100


        grand_total = total + tax  
        
        all_coupons = Coupon.objects.all()
        list_coupon=[]

            # Iterate through each coupon
        current_date = timezone.now().date()
        for coupon in all_coupons:
            # Check if grand_total is within the coupon's range
            if coupon.minimum_purchase <= grand_total <= coupon.maximum_purchase:
                if coupon.expiry_date and current_date <= coupon.expiry_date:
                    
                    list_coupon.append(coupon)

    
    except ObjectDoesNotExist:
        pass
        
    
                    
        
        
    

    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'addresses':adress,
        'tax': tax,
        'grand_total': grand_total,
        #'coupons'  : coupons,
        'list_coupon': list_coupon,
        'selected_coupon_id': None,
        
    }


    return render(request,'user/cartcheckout.html',context)
        
   


def remove_cart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, product_id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            variant = cart_item.variations
            variant.stock += 1
            cart_item.quantity -= 1

            variant.save()
            cart_item.save()    
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart:shopping_cart')



def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, product_id=product_id)

    try:
        if request.user.is_authenticated:
            # If the user is authenticated, remove the cart item associated with the user
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            # If the user is not authenticated, remove the cart item associated with the session cart
            cart_item = CartItem.objects.get(product=product, cart__cart_id=_cart_id(request), id=cart_item_id)
        
        # Delete the cart item
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # Handle the case where the cart item doesn't exist

    # Redirect back to the shopping cart page
    return redirect('baseapp:mycart')





 
def newcart_update(request):
    print("working plus")
    new_quantity = 0
    total = 0
    tax = 0
    grand_total = 0
    quantity=0
    counter=0

    if request.method == 'POST' and request.user.is_authenticated:
        prod_id = int(request.POST.get('product_id'))
        cart_item_id = int(request.POST.get('cart_id'))
        qty=int(request.POST.get('qty'))
        counter=int(request.POST.get('counter'))
        print(qty)
        product = get_object_or_404(Product, product_id=prod_id)

        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        cart_items = CartItem.objects.filter(user=request.user)
        
        
    
        variation = cart_item.variations  # Access the variation associated with the cart item
        if cart_item.quantity < cart_item.variations.stocks:

                cart_item.quantity += 1
                cart_item.save()
                
                pr=cart_item.product.get_final_price()
                sub_total=cart_item.quantity * pr
                new_quantity = cart_item.quantity
        else:
                message = "out of stock"
                return JsonResponse({'status': 'error', 'message': message})      
        for cart_item in cart_items:
            pr=cart_item.product.get_final_price()
            total += (pr * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
        print(new_quantity,total,tax,grand_total,sub_total)       
        
        

    if new_quantity ==0:
        message = "out of stock"
        return JsonResponse({'status': 'error', 'message': message})
    else:
        return JsonResponse({
            'status': "success",
            'new_quantity': new_quantity,
            "total": total,
            "tax": tax,
            'counter':counter,
            "grand_total": grand_total,
            "sub_total":sub_total,
            
        })








def remove_cart_item_fully(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            counter = int(request.POST.get('counter'))
            product_id = int(request.POST.get('product_id'))
            cart_item_id = int(request.POST.get('cart_id'))

            # Get the product and cart item
            product = get_object_or_404(Product, product_id=product_id)
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
            cart_items = CartItem.objects.filter(user=request.user)

            # Check if the cart item exists and belongs to the logged-in user
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                pr=cart_item.product.get_final_price()
                sub_total = cart_item.quantity * pr

                total = 0
                quantity = 0

                for cart_item in cart_items:
                    pr=cart_item.product.get_final_price()
                    total += (pr* cart_item.quantity)
                    quantity += cart_item.quantity

                tax = (2 * total) / 100
                grand_total = total + tax
                current_quantity = cart_item.quantity

                return JsonResponse({
                    'status': 'success',
                    'tax': tax,
                    'total': total,
                    'grand_total': grand_total,
                    'counter': counter,
                    'new_quantity': current_quantity,
                    'sub_total': sub_total,  # Updated quantity
                })
            else:
                cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
                cart_item.delete()
                message = "the cart item has bee deleted"
                return JsonResponse({'status': 'error', 'message': message}) 

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return HttpResponseBadRequest('Invalid request')

def set_default_address(request, address_id):
    user = request.user

    # Ensure that the address belongs to the user
    address = get_object_or_404(Address, id=address_id, user=user)

    # Set the selected address as default
    user.addresses.filter(is_default=True).update(is_default=False)
    address.is_default = True
    address.save()

    return redirect('cart:checkout')


def addtowishlist(request,product_id):
    
    if not request.user.is_authenticated:
        return redirect('baseapp:login')
    
    product = get_object_or_404(Product, product_id=product_id)
    variant = get_object_or_404(Variant, product=product)

    # Try to get the existing wishlist for the user
    wishlist = Wishlist.objects.filter(user=request.user,product=product,variations=variant)

    if wishlist:
        messages.error(request,'product already exist')
        product_detail_url = reverse('baseapp:gotoproduct', args=[product_id])
        return redirect(product_detail_url)
    else:
        # Create a new wishlist for the user
        Wishlist.objects.create(user=request.user, product=product, variations=variant)

    product_detail_url = reverse('baseapp:gotoproduct', args=[product_id])
    return redirect(product_detail_url)


@never_cache
def apply_coupon(request, total=0, quantity=0, cart_items=None):
    if not request.user.is_authenticated:
        return redirect('baseapp:login')

    list_coupon = []
    
        # Initialize variables
    tax = 0
    grand_total = 0
    coupon_discount = 0
    selected_coupon_id = request.GET.get('coupon_code')
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        adress = Address.objects.filter(user=request.user)
    else:
        addresses = []
    for cart_item in cart_items:
        pr=cart_item.product.get_final_price()
        total += (pr * cart_item.quantity)
        quantity += cart_item.quantity
        try:
            if cart_item.variations.stocks <= 0:
                print("Not enough stock!")
        except ObjectDoesNotExist:
            pass
    tax = (2 * total) / 100
    user = request.user
    try:
        final_coupon = Coupon.objects.get(pk=selected_coupon_id)
    except Coupon.DoesNotExist:
        # Handle the case where the coupon with the given ID doesn't exist
        print("Selected coupon does not exist.")
        final_coupon = None
    try:
        rcoupon = Redeemed_Coupon.objects.get(user=user)
    except Redeemed_Coupon.DoesNotExist:
    # If the Redeemed_Coupon doesn't exist for the user, create a new instance
    # Assuming Coupon.objects.first() returns a valid Coupon instance, modify this part based on your actual logic.
        coupon_instance = Coupon.objects.get(pk=selected_coupon_id)
        rcoupon = Redeemed_Coupon.objects.create(user=user, coupon=coupon_instance)
    # Calculate grand_total after updating dummy_count
   # Calculate grand_total after updating dummy_count
    grand_total = total + tax - float(final_coupon.coupon_amount) if final_coupon else 0
    if grand_total<1:
        return redirect('baseapp:product')

    print('akhi',grand_total)
    
    all_coupons = Coupon.objects.all()
    
    # Iterate through each coupon
    current_date = timezone.now().date()
    for coupon in all_coupons:
            # Check if grand_total is within the coupon's range
            if coupon.minimum_purchase <= grand_total <= coupon.maximum_purchase:
                if coupon.expiry_date and current_date <= coupon.expiry_date:
                    
                    list_coupon.append(coupon)

   

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'addresses': adress,
        'tax': tax,
        'grand_total': grand_total,
        'list_coupon': list_coupon,
        'temp': 0,
        'coupon_ids': selected_coupon_id
    }

    return render(request, 'user/cartcheckout.html', context)

        