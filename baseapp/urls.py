from django.contrib import admin
from django.urls import path,include
from . import views

app_name='baseapp'

urlpatterns = [
    path('',views.index,name='index'),
    path('index/',views.index,name='index'),
    path('login/',views.handlelogin,name='login'),
    path('signup/',views.signup,name='signup'),
    path('product/',views.products,name='product'),
    path('sp/',views.sent_otp,name='sp'),
    path('vp/',views.verify_otp,name='vp'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('base/',views.base,name='base'),
    path('admin_pannel/',views.admin_login,name='admin_pannel'), 
    path('alogout/',views.admin_logout,name='alogout'),
    path('db/',views.db,name='db'),
    # path('product_info',views.product_info,name='product_info'),
    path('product_detail/<int:product_id>/',views.product_detail,name='product_detail'),
    path('gotoproduct/<int:product_id>/',views.gotoproduct,name='gotoproduct'),
    path('resend_otp_view/',views.resend_otp,name='resend_otp_view'),
    
    
    
    path('userprofile/',views.user_profile,name='userprofile'),
    path('mycart/',views.mycart,name='mycart'),
    path('manageaddress/',views.manageaddress,name='manageaddress'),
    path('addaddress/',views.addaddress,name='addaddress'),
    path('showorder/',views.showorder,name='showorder'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('coupons/',views.coupons,name='coupons'),
    path('setdefaultaddress/<int:address_id>/', views.set_default_address, name='setdefaultaddress'),
    
    
    

    path('edituserinfo/',views.edituserinfo,name='edituserinfo'),
    path('deleteadress/<int:id>',views.deleteadress,name='deleteadress'),
    
    
    path('wallet/',views.wallet,name='wallet'),
    path('wishlist/',views.wishlist,name='wishlist'),
    
    path('invite/', views.invite, name='invite'),
    path('remove_wishlist/<int:item_id>',views.remove_wishlist,name='remove_wishlist')
    
    
    
    
    
    
    
    
]
