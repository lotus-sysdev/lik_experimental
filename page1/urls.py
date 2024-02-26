from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', placeholder,name='index'),

    # form add urls
    path('add_customer/', add_customer, name='add_customer'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('add_item/',add_item, name='add_item'),
    path('add_PO/', add_PO, name='add_PO'),
    path('add_WO/', add_WO, name='add_WO'),

    # display customer, supplier, and item tables
    path('display_customer/',display_customer, name='display_customer'),
    path('display_supplier/',display_supplier, name='display_supplier'),
    path('display_item/', display_item, name="display_item"),

    # display purchase and work
    path('display_purchase/',display_purchase, name='display_purchase'),
    path('display_work/',display_work, name='display_work'),

    # purchase and work detail, edit, and delete
    path('purchase_detail/<int:id>/', purchase_detail, name='purchase_detail'),
    path('work_detail/<int:id>/', work_detail, name='work_detail'),
    path('edit_purchase/<int:id>/', edit_purchase, name='edit_purchase'),
    path('edit_work/<int:id>/', edit_work, name='edit_work'),
    path('delete_purchase/<int:id>/', delete_purchase, name='delete_purchase'),
    path('delete_work/<int:id>/', delete_work, name='delete_work'),

    # customer detail, edit, and delete
    path('customer_detail/<int:cust_id>/', customer_detail, name='customer_detail'),
    path('edit_customer/<int:cust_id>/', edit_customer, name='edit_customer'),
    path('delete_customer/<int:cust_id>/', delete_customer, name='delete_customer'),

    # supplier detail, edit, and delete
    path('supplier_detail/<int:supp_id>/', supplier_detail, name='supplier_detail'),
    path('edit_supplier/<int:supp_id>/', edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:supp_id>/', delete_supplier, name='delete_supplier'),
    
    # item detail, edit, and delete
    path('item_detail/<int:SKU>/', item_detail, name='item_detail'),
    path('edit_item/<int:SKU>/', edit_item, name='edit_item'),
    path('delete_item/<int:SKU>/', delete_item, name='delete_item'),	
    
    # Sumber url
    path('add_sumber/<int:SKU>',add_sumber, name='add_sumber'),
    
    # PIC urls
    path('add_pic_cust/<int:cust_id>',add_customer_pic,name='add_pic_cust'),
    path('add_pic_supp/<int:supp_id>',add_supplier_pic,name='add_pic_supp'),

    # Alamat urls
    path('add_customer_alamat/<int:cust_id>/', add_customer_alamat, name='add_customer_alamat'),
    path('add_supplier_alamat/<int:supp_id>/', add_supplier_alamat, name='add_supplier_alamat'),
    
    # Login, Register, and Logou
    path('login/',login_view, name="login"),
    path('register/',register_view, name="register"),
    path('logout/', logout_view, name='logout'),
]

