from django.db import models
import uuid

# Create your models here.
class Customer(models.Model):
    cust_id = models.IntegerField(primary_key=True)
    nama_pt = models.CharField(max_length=255)
    alamat_penagihan = models.CharField(max_length=255)
    alamat_pengiriman = models.CharField(max_length=255)
    telp = models.PositiveIntegerField()
    # pic = models.ForeignKey('PIC', on_delete=models.CASCADE, related_name='customers', null=True)
    terms_of_payment = models.CharField(max_length=10)
    pengiriman = models.CharField(max_length=50)
    npwp = models.CharField(max_length=255)
    faktur = models.BooleanField()

class Supplier(models.Model):
    supp_id = models.IntegerField(primary_key = True)
    nama_pt = models.CharField(max_length=255)
    alamat_penagihan = models.CharField(max_length=255)
    alamat_pengiriman = models.CharField(max_length=255)
    telp = models.PositiveIntegerField()
    # pic = models.ForeignKey('PIC', on_delete=models.CASCADE, related_name='customers', null=True)
    terms_of_payment = models.CharField(max_length=10)
    pengiriman = models.CharField(max_length=50)
    npwp = models.CharField(max_length=255)
    faktur = models.BooleanField()

class PIC(models.Model):
    PIC_Id = models.IntegerField(primary_key = True, unique = True)
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    telp = models.PositiveIntegerField()
    Role = models.CharField(max_length=50)
