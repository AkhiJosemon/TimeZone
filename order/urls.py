from django.urls import path,include,re_path
from . import views
app_name='order'

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    
    
    path('order_success', views.order_success, name='order_success'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('return_order/<int:order_id>/', views.return_order, name='return_order'),
    path('confirm_razorpay_payment/', views.online_place_order, name='confirm_razorpay_payment'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    re_path(r'^pay_with_wallet/(?P<g_total>[\d.]+)/$', views.pay_with_wallet, name='pay_with_wallet'),

   
    
]