from django.urls import path
from .views import *

urlpatterns = [
    path('', placeholder,name='index'),
    path('my-form/', my_view, name='my-form'),
    path('datatb/',display_customer, name='datatb')
]
