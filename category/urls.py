from django.urls import path,include
from category import views

app_name = 'category'


urlpatterns =[

    path('catogory_list/',views.catagory_list,name='catogory_list'),
    path('add_catogory/',views.add_catagory,name='add_catogory'),
    path('sub_add_catogory/',views.sub_add_catagory,name='sub_add_catogory'),
    path('insert_catogory/',views.insert_catagoriy,name='insert_catogory'),
    path('insert_sub_catogory/',views.insert_sub_catagoriy,name='insert_sub_catogory'),
    
    path('delete-category/<slug:slug>/', views.delete_category, name='delete_category'),
    path('sub_delete_category/<slug:slug>/', views.sub_delete_category, name='sub_delete_category'),
    
    path('edit_catagory/<str:category_name>/', views.edit_catagory, name='edit_catagory'),
    path('sub_edit_catagory/<str:category_name>/', views.sub_edit_catagory, name='sub_edit_catagory'),
    
    path('user_list',views.user_list,name='user_list'),
    path('action_user/<int:user_id>/', views.action_user, name='action_user'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_list/',views.produ,name='product_list'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('brand/',views.brand,name='brand'),
    path('add_brand/',views.insert_brand,name='add_brand'),
    path('delete-brand/<str:slug>/', views.delete_brand, name='delete_brand'),
    #path('edit_brand/<str:brand_name>/', views.edit_brand, name='edit_brand'),
    path('brand_list/',views.brand_list,name='brand_list'),
    path('variant_list/',views.variant_list,name='variant_list'),
    path('add_variant/',views.add_variant,name='add_variant'),
    # path('edit_variant/',views.edit_variant,name='edit_variant'),
    path('coupons_list/',views.coupons_list,name='coupons_list'),
    path('add_coupons/',views.add_coupons,name='add_coupons'),
    
    
   
    path('Order_list/',views.Order_list,name='Order_list'),
    path('update_order_status/<int:order_id>',views.update_order_status,name='update_order_status'),
    #path('change_password/',views.change_password,name='change_password'),
    path('edit_variant/<int:var_id>',views.edit_variant,name='edit_variant'),
    path('delete_variant/<int:var_id>',views.delete_variant,name='delete_variant'),
    path('delete_coupon/<int:coup_id>',views.delete_coupon,name='delete_coupon'),
    path('edit_coupon/<int:coup_id>',views.edit_coupon,name='edit_coupon'),
    path('add_product_offer/<int:product_id>/',views.add_product_offer, name='add_product_offer'),
    path('add_category_offer/<int:category_id>/',views.add_category_offer, name='add_category_offer'),
    path('productofferpage',views.productofferpage,name='productofferpage'),
    path('categoryofferpage',views.categoryofferpage,name='categoryofferpage'),
    path('productofferlist',views.productofferlist,name='productofferlist'),
    path('categoryofferlist',views.categoryofferlist,name='categoryofferlist'),
    path('delete_productoffer/<int:off_id>/',views.delete_productoffer,name='delete_productoffer')
    
    
    
    
    
    



]