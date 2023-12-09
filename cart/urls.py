from django.urls import path,include
from . import views
app_name='cart'

urlpatterns = [
    path('addtocart/<int:product_id>/', views.addtocart, name='addtocart'),
    path('addtowishlist/<int:product_id>/',views.addtowishlist,name='addtowishlist'),
    path('checkout/',views.cartcheckout,name='checkout'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('newcart_update',views.newcart_update,name='newcart_update'),
    path('remove_cart_item_fully',views.remove_cart_item_fully,name='remove_cart_item_fully'),
    path('setdefaultaddress/<int:address_id>/', views.set_default_address, name='setdefaultaddress'),
    path('apply_coupon/',views.apply_coupon,name='apply_coupon'),
]