# urls.py

from django.urls import path
from .views import add_customer

urlpatterns = [
    path('my-form/', add_customer, name='my-form'),
]
