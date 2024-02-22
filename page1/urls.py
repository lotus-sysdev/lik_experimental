from django.urls import path
from .views import *
from django_select2.views import AutoResponseView

urlpatterns = [
    path('', placeholder,name='index'),

    # form urls
    path('add_customer/', add_customer, name='add_customer'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('add_item/',add_item, name='add_item'),
    

    # display customer, supplier, and item tables
    path('display_customer/',display_customer, name='Customer Data'),
    path('display_supplier/',display_supplier, name='Supplier Data'),
    path('display_item/', display_item, name="Item Data"),

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
    
    # PIC urls
    path('add_pic_cust/<int:cust_id>',add_customer_pic,name='add_pic_cust'),
    path('add_pic_supp/<int:supp_id>',add_supplier_pic,name='add_pic_supp'),

    path('add_sumber/<int:SKU>',add_sumber, name='add_sumber'),

    # Alamat urls
    path('add_customer_alamat/<int:cust_id>/', add_customer_alamat, name='add_customer_alamat'),
    path('add_supplier_alamat/<int:supp_id>/', add_supplier_alamat, name='add_supplier_alamat'),

    path('add_PO/', add_PO, name='add_PO'),

    path('select2/', AutoResponseView.as_view(model='Items'), name='select2_view'),
]
