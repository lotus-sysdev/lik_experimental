import datetime
from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField

# Create your models here.
class Customer(models.Model):
    cust_id = models.IntegerField(primary_key=True)
    nama_pt = models.CharField(max_length=255)
    telp = PhoneNumberField()
    terms_of_payment = models.CharField(max_length=10)
    pengiriman = models.CharField(max_length=50)
    npwp = models.CharField(max_length=255)
    faktur = models.BooleanField()

    def __str__(self):
        return self.nama_pt

class Supplier(models.Model):
    supp_id = models.IntegerField(primary_key = True)
    nama_pt = models.CharField(max_length=255)
    telp = PhoneNumberField()
    terms_of_payment = models.CharField(max_length=10)
    npwp = models.CharField(max_length=255)
    faktur = models.BooleanField()

    def __str__(self):
        return self.nama_pt

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
    price = MoneyField(max_digits=15, default_currency='IDR', )
    gambar = models.ImageField()
    
    def __str__(self):
        return self.nama

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

def default_date():
    return datetime.date(1900, 1, 1)

class PurchaseOrder(models.Model):
    supplier= models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    revenue_PO = MoneyField(max_digits=15, default_currency='IDR', blank=True, null=True, default=0)
    nomor_PO = models.IntegerField(blank=True, null=True, default=0)
    tanggal_PO = models.DateField(blank=True, null=True, default=default_date)
    tanggal_process = models.DateField(blank=True, null=True, default=default_date)
    tanggal_input_accurate = models.DateField(blank=True, null=True, default=default_date)
    tanggal_pengiriman_barang = models.DateField(blank=True, null=True, default=default_date)
    tanggal_pengiriman_invoice = models.DateField(blank=True, null=True, default=default_date)
    STATUS_CHOICES = (
        ('order', 'Order Created'),
        ('pending', 'Pending'),
        ('process', 'Process'),
        ('accurate', 'Accurate'),
        ('pengiriman', 'Pengiriman Barang'),
        ('invoice', 'Pengiriman Invoice'),
        ('complete', 'Completed')
    )
    status = models.CharField(max_length=30,choices = STATUS_CHOICES) 
    STATUS_CONDITIONS = {
        'complete': lambda self: self.tanggal_pengiriman_invoice and self.tanggal_pengiriman_barang and self.tanggal_input_accurate and self.tanggal_process and self.tanggal_PO and self.revenue_PO and self.nomor_PO,
        'invoice': lambda self: self.tanggal_pengiriman_invoice,
        'pengiriman': lambda self: self.tanggal_pengiriman_barang,
        'accurate': lambda self: self.tanggal_input_accurate,
        'process': lambda self: self.tanggal_process,
        'order': lambda self: self.revenue_PO or self.nomor_PO or self.tanggal_PO,
        'pending': lambda self: True,
    }

    def save(self, *args, **kwargs):
        # Update the status based on conditions
        for status, condition in self.STATUS_CONDITIONS.items():
            if condition(self):
                self.status = status
                break

        super(PurchaseOrder, self).save(*args, **kwargs)

class WorkOrder(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    revenue_PO = MoneyField(max_digits=15, default_currency='IDR', blank=True, null=True, default=0)
    nomor_PO = models.IntegerField(blank=True, null=True, default=0)
    tanggal_PO = models.DateField(blank=True, null=True, default=default_date)
    tanggal_process = models.DateField(blank=True, null=True, default=default_date)
    tanggal_input_accurate = models.DateField(blank=True, null=True, default=default_date)
    tanggal_pengiriman_barang = models.DateField(blank=True, null=True, default=default_date)
    tanggal_pengiriman_invoice = models.DateField(blank=True, null=True, default=default_date)
    STATUS_CHOICES = (
        ('order', 'Order Created'),
        ('pending', 'Pending'),
        ('process', 'Process'),
        ('accurate', 'Accurate'),
        ('pengiriman', 'Pengiriman Barang'),
        ('invoice', 'Pengiriman Invoice'),
        ('complete', 'Completed')
    )
    status = models.CharField(max_length=30,choices = STATUS_CHOICES) 
    STATUS_CONDITIONS = {
        'complete': lambda self: self.tanggal_pengiriman_invoice and self.tanggal_pengiriman_barang and self.tanggal_input_accurate and self.tanggal_process and self.tanggal_PO and self.revenue_PO and self.nomor_PO,
        'invoice': lambda self: self.tanggal_pengiriman_invoice,
        'pengiriman': lambda self: self.tanggal_pengiriman_barang,
        'accurate': lambda self: self.tanggal_input_accurate,
        'process': lambda self: self.tanggal_process,
        'order': lambda self: self.revenue_PO or self.nomor_PO or self.tanggal_PO,
        'pending': lambda self: True,
    }

    def save(self, *args, **kwargs):
        # Update the status based on conditions
        for status, condition in self.STATUS_CONDITIONS.items():
            if condition(self):
                self.status = status
                break

        super(WorkOrder, self).save(*args, **kwargs)