from django.urls import path
from .views import *

urlpatterns = [
    path('', placeholder,name='index'),
    path('add_customer/', add_customer, name='add_customer'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('display_customer/',display_customer, name='Customer Data'),
    path('display_supplier/',display_supplier, name='Supplier Data'),
    path('customer_detail/<int:cust_id>/', customer_detail, name='customer_detail'),
    path('edit_customer/<int:cust_id>/', edit_customer, name='edit_customer'),
    path('delete_customer/<int:cust_id>/', delete_customer, name='delete_customer'),
    path('supplier_detail/<int:supp_id>/', supplier_detail, name='supplier_detail'),
    path('edit_supplier/<int:supp_id>/', edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:supp_id>/', delete_supplier, name='delete_supplier'),
]
