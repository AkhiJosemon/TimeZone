from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect
from .forms import PaymentMethodForm
from .models import Order, OrderProduct
from baseapp.models import *
from django.contrib import messages
from cart.models import *
from datetime import datetime, date
from .models import *
import datetime
import random
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from datetime import datetime, timedelta
import json
from django.db.models import Sum
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.db.models.functions import TruncDate
import datetime
from django.views.decorators.cache import cache_control

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request):
    if request.method=='POST':
        current_user=request.user
        grand_total=request.POST.get('grand_total')
        total=request.POST.get('total')
        tax=request.POST.get('tax')
        cart=request.POST.get('cart_id')
        adress=Address.objects.filter(user=request.user, is_default=True).first()
        short_id = str(random.randint(1000, 9999))
        print(grand_total,total,tax,cart)   
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
       
        current_date = d.strftime("%Y%m%d")
        order_numbers = current_date + short_id 
        

         
        
        var=Order.objects.create(
            user=request.user,
            # payment='cash on delivery',
            order_number=order_numbers,
            order_total= grand_total,
            tax=tax,
            selected_address=adress,
            ip=request.META.get('REMOTE_ADDR')
            
            
        )
        var.save()
        
        payment=Payment.objects.create(
            user=request.user,
            payment_method='cash on delivery ',
            amount_paid= grand_total,
            status='pending',
            
        )
        var.payment=payment
        var.save()
        
        
        cart=CartItem.objects.filter(user=request.user)
        
        for item in cart:
            orderedproduct=OrderProduct()
            item.variations.stocks-=item.quantity
            item.variations.save()
            orderedproduct.order=var
            orderedproduct.payment=payment
            orderedproduct.user=request.user
            orderedproduct.product=item.product
            orderedproduct.quantity=item.quantity
            orderedproduct.product_price=item.product.price
            orderedproduct.ordered=True
            orderedproduct.save()
            cart.delete()
       
            
    return redirect("order:order_success")




def online_place_order(request):
    if request.method=='POST':
        current_user=request.user
        grand_total=request.POST.get('grand_total')
        total=request.POST.get('total')
        tax=request.POST.get('tax')
        cart=request.POST.get('cart_id')
        adress=Address.objects.filter(user=request.user, is_default=True).first()
        short_id = str(random.randint(1000, 9999))
        print(grand_total,total,tax,cart)   
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_numbers = current_date + short_id 
        

         
        
        var=Order.objects.create(
            user=request.user,
            # payment='cash on delivery',
            order_number=order_numbers,
            order_total= grand_total,
            tax=tax,
            selected_address=adress,
            ip=request.META.get('REMOTE_ADDR')
            
            
        )
        var.save()
        
        payment=Payment.objects.create(
            user=request.user,
            payment_method='razor_pay',
            amount_paid= grand_total,
            status='paid',
            
        )
        var.payment=payment
        var.save()
        
        
        cart=CartItem.objects.filter(user=request.user)
        
        for item in cart:
            orderedproduct=OrderProduct()
            item.variations.stocks-=item.quantity
            item.variations.save()
            orderedproduct.order=var
            orderedproduct.payment=payment
            orderedproduct.user=request.user
            orderedproduct.product=item.product
            orderedproduct.quantity=item.quantity
            orderedproduct.product_price=item.product.price
            orderedproduct.ordered=True
            orderedproduct.save()
            cart.delete()
        #return HttpResponse('success')
        # return redirect()
             
    return redirect("order:order_success")

def pay_with_wallet(request,g_total):
    
        # Check if the user has a wallet
        user = request.user
        wallet = Wallet.objects.get(user=user)

        # Get the grand total from the request
        
        grand_total=float(g_total)
        if wallet.wallet_amount >= grand_total:
            # Deduct the amount from the wallet
            wallet.wallet_amount -= grand_total
            wallet.save()

            # Process the order (you can customize this part according to your needs)
            # ...

            return redirect('order:order_success')  # Redirect to order success page

        else:
            error_message = 'Insufficient funds in the wallet. Please choose another payment method.'
        
        # Store the error message in the session
            messages.error(request, error_message)

        # Redirect to checkout page
            return redirect(reverse('cart:checkout'))
    

def order_success(request):
    order = Order.objects.filter(user=request.user).order_by('-id').first()
    
    
    context = {
        'order_number': order.order_number,
        'order_status': order.status,
    }
   
   
    return render(request,'user/order_sucess.html',context)

def cancel_order(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)

    
    order.status = 'Cancelled'
    order.save()

   
    return redirect('baseapp:showorder')

def return_order(request, order_id):
    
    order = Order.objects.get(id=order_id)
    order_method=order.payment.payment_method
    if  order_method!='Cash on Delivery'and order.status == 'Delivered':
        user_profile = request.user
        wallets,create = Wallet.objects.get_or_create(user=user_profile)

        # Credit the purchased amount back to the wallet
        wallets.wallet_amount += order.order_total
        wallets.wallet_amount = round(wallets.wallet_amount, 2)
        wallets.save()
       
        # Update the order status to 'Returned'
        order.status = 'Rejected'
        order.save()
        order_products = OrderProduct.objects.filter(order=order)
        for order_product in order_products:
            product = order_product.product.product_id
            product_variants = Variant.objects.filter(product_id=product)
                        
            for variant in product_variants:
             variant.stocks += order_product.quantity
             variant.save()
        messages.warning(request, 'return request has been send. amount sucessfully returned to your wallet')

    elif order_method=='Cash on Delivery' and order.status == 'Completed':
        order.status = 'Rejected'
        order.save()
        messages.warning(request, 'return request has been send.')

    elif order_method=='Cash on Delivery' and order.status != 'Completed' :
        order.status = 'Cancelled'
        order.save()
        messages.warning(request, 'return request has been send.')
    else:
        user_profile = request.user
        wallets,create = Wallet.objects.get_or_create(user=user_profile)

        # Credit the purchased amount back to the wallet
        wallets.wallet_amount += order.order_total
        wallets.wallet_amount = round(wallets.wallet_amount, 2)
        wallets.save()
       
        # Update the order status to 'Returned'
        order.status = 'Cancelled'
        order.save()
        order_products = OrderProduct.objects.filter(order=order)
        for order_product in order_products:
            product = order_product.product.product_id
            product_variants = Variant.objects.filter(product_id=product)
                        
            for variant in product_variants:
             variant.stocks += order_product.quantity
             variant.save()
        messages.warning(request, 'cancel request has been send. amount sucessfully returned to your wallet')
   
    return redirect('baseapp:showorder')

def sales_report(request):
    if not request.user.is_authenticated:
        return redirect('base:admin_pannel')

    if request.method == 'POST':
        from_date = request.POST.get('fromDate')
        to_date = request.POST.get('toDate')
        time_period = request.POST.get('timePeriod')

        # Check for empty or missing dates
        if not from_date or not to_date:
            return HttpResponseBadRequest("Please provide valid date values.")

        # Convert date strings to datetime objects
        try:
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
        except ValueError:
            return HttpResponseBadRequest("Invalid date format.")

        # Calculate sales data based on time period
        if time_period == 'all':
            sales_data = Order.objects.filter(created_at__range=[from_date, to_date]) \
                .values('created_at__date') \
                .annotate(total_orders=Count('id'), total_revenue=Sum('order_total'))
        elif time_period == 'daily':
            sales_data = Order.objects.filter(created_at__range=[from_date, to_date]) \
                .values('created_at__date') \
                .annotate(total_orders=Count('id'), total_revenue=Sum('order_total'))
        elif time_period == 'weekly':
            sales_data = Order.objects.filter(created_at__range=[from_date, to_date]) \
                .extra({'week': "date_trunc('week', created_at)"}).values('week') \
                .annotate(total_orders=Count('id'), total_revenue=Sum('order_total'))
        elif time_period == 'monthly':
            sales_data = Order.objects.filter(created_at__range=[from_date, to_date]) \
                .extra({'month': "date_trunc('month', created_at)"}).values('month') \
                .annotate(total_orders=Count('id'), total_revenue=Sum('order_total'))
        elif time_period == 'yearly':
            sales_data = Order.objects.filter(created_at__range=[from_date, to_date]) \
                .extra({'year': "date_trunc('year', created_at)"}).values('year') \
                .annotate(total_orders=Count('id'), total_revenue=Sum('order_total'))

        # Define the dateWise queryset for daily sales data
        dateWise = Order.objects.filter(created_at__range=[from_date, to_date]) \
            .values('created_at__date') \
            .annotate(total_orders=Count('id'), total_revenue=Sum('order_total'))

        # Calculate Total Users
        total_users = Order.objects.filter(is_ordered=True).values('user').distinct().count()

        # Calculate Total Products
        total_products = OrderProduct.objects.filter(order__is_ordered=True).values('product').distinct().count()

        # Calculate Total Orders
        total_orders = Order.objects.filter(is_ordered=True).count()

        # Calculate Total Revenue
        total_revenue = Order.objects.filter(is_ordered=True).aggregate(total_revenue=Sum('order_total'))['total_revenue']

        
        print("Total Users:", total_users)
        print("Total Products:", total_products)
        print("Total Orders:", total_orders)
        print("Total Revenue:", total_revenue)


        context = {
            'sales_data': sales_data,
            'from_date': from_date,
            'to_date': to_date,
            'report_type': time_period,
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'dateWise': dateWise,
        }

        return render(request, 'admin/sales_report.html', context)

    return render(request, 'admin/sales_report.html')
    
    
def admin_dashboard(request):
    if request.user.is_authenticated:
        if not request.user.is_superadmin:
            return redirect('baseapp:admin_pannel')
    # Example: Retrieve total number of orders
    total_orders = Order.objects.count()

    # Example: Retrieve total revenue
    total_revenue = Order.objects.aggregate(Sum('order_total'))['order_total__sum'] or 0

    # Example: Retrieve recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]

    return render(request, 'admin/admin_dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
    })
    


