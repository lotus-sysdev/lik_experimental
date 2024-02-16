from django.urls import path
from .views import *

urlpatterns = [
    path('', placeholder,name='index'),
    path('my-form/', my_view, name='my-form'),
    path('display-cus/',display_customer, name='Customer Data'),
    path('display-sup/',display_supplier, name='Supplier Data'),
]
