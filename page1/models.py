from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Customer(models.Model):
    cust_id = models.IntegerField(primary_key=True)
    nama_pt = models.CharField(max_length=255)
    telp = PhoneNumberField()
    terms_of_payment = models.CharField(max_length=10)
    pengiriman = models.CharField(max_length=50)
    npwp = models.CharField(max_length=255)
    faktur = models.BooleanField()

class Supplier(models.Model):
    supp_id = models.IntegerField(primary_key = True)
    nama_pt = models.CharField(max_length=255)
    telp = PhoneNumberField()
    terms_of_payment = models.CharField(max_length=10)
    npwp = models.CharField(max_length=255)
    faktur = models.BooleanField()

class CustomerPIC(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    telp = PhoneNumberField()
    Role = models.CharField(max_length=50)

class SupplierPIC(models.Model):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    telp = PhoneNumberField()
    Role = models.CharField(max_length=50)

class Items(models.Model):
    SKU = models.IntegerField(primary_key = True, unique = True)
    nama = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.IntegerField()
    gambar = models.ImageField()

class ItemSumber(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('online', 'Online Store'),
        ('pabrik', 'Pabrik'),
    )
    jenis_sumber = models.CharField(max_length=30, choices=TYPE_CHOICES)
    nama_perusahaan = models.CharField(max_length=255)
    telp = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    
class CustomerAlamat(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('penagihan', 'Alamat Penagihan'),
        ('pengiriman', 'Alamat Pengiriman'),
    )
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    provinsi = models.CharField(max_length=255)
    kota = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    kelurahan = models.CharField(max_length=50)
    detail = models.CharField(max_length=50)

class SupplierAlamat(models.Model):
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('penagihan', 'Alamat Penagihan'),
        ('pengiriman', 'Alamat Pengiriman'),
    )
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    provinsi = models.CharField(max_length=255)
    kota = models.CharField(max_length=50)
    kecamatan = models.CharField(max_length=50)
    kelurahan = models.CharField(max_length=50)
    detail = models.CharField(max_length=50)