from django.urls import path
from .views import *

urlpatterns = [
    path('', placeholder,name='index'),
    path('my-form/', my_view, name='my-form'),
]
