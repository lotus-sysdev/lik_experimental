from django.urls import path
from .views import *

urlpatterns = [
    path('', placeholder,name='index'),

    # form urls
    path('add_customer/', add_customer, name='add_customer'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('add_pic/',add_pic, name='add_pic'),
    path('add_item/',add_item, name='add_item'),

    # display customer and supplier tables
    path('display_customer/',display_customer, name='Customer Data'),
    path('display_supplier/',display_supplier, name='Supplier Data'),

    # customer detail, edit, and delete
    path('customer_detail/<int:cust_id>/', customer_detail, name='customer_detail'),
    path('edit_customer/<int:cust_id>/', edit_customer, name='edit_customer'),
    path('delete_customer/<int:cust_id>/', delete_customer, name='delete_customer'),

    # supplier detail, edit, and delete
    path('supplier_detail/<int:supp_id>/', supplier_detail, name='supplier_detail'),
    path('edit_supplier/<int:supp_id>/', edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:supp_id>/', delete_supplier, name='delete_supplier'),

    # Items
    path('display_item/', display_item, name="Item Data")
    
]
