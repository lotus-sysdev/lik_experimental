import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField
from django_measurement.models import MeasurementField
from measurement.measures import Mass

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

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Items(models.Model):
    SKU = models.CharField(max_length=10, primary_key = True, unique = True)
    nama = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10)
    price = MoneyField(max_digits=15, default_currency='IDR', )
    gambar = models.ImageField()
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        if not self.SKU or 'is_approved' in kwargs:
            # Generate SKU based on category and a unique number
            if self.category and 'is_approved' not in kwargs:
                category_code = self.category.name[:3].upper()  # Take the first three letters of the category

                # Retrieve the last SKU in the same category
                last_sku = Items.objects.filter(category=self.category).order_by('-SKU').first()

                if last_sku and last_sku.SKU:
                    last_number_str = str(last_sku.SKU)[3:]  # Extract the number part of the SKU
                    if last_number_str.isdigit():
                        last_number = int(last_number_str)
                    else:
                        last_number = 0
                else:
                    last_number = 0

                new_sku = f"{category_code}{last_number + 1:04d}"  # Combine category code and a 4-digit number
                self.SKU = new_sku

        super().save(*args, **kwargs)

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

class UserActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255)
    payload = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.action} - {self.timestamp}'
    
class Messenger(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length = 10, default = "#3a87ad")

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    id = models.AutoField(primary_key=True)
    model = models.CharField(max_length = 100)
    JENIS_CHOICES = (
        ("truck", "Truck"),
        ("mobil", "Mobil"),
        ("motor", "Motor"),
        ("ojek_online", "Ojek Online")
    )
    jenis = models.CharField(max_length=20)
    nomor_plat = models.CharField(max_length = 9)

    def __str__(self):
        return self.nomor_plat
class Events(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, null = True)
    start = models.DateTimeField(null = True, blank = True)
    end = models.DateTimeField(null = True, blank = True)
    messenger = models.ForeignKey(Messenger,on_delete=models.SET_NULL, null=True)
    start_location = models.CharField(max_length=255, null =True)
    destination = models.CharField(max_length=255, null =True)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.SET_NULL, null=True)
    package_name = models.CharField(max_length=100, null=True)
    package_dimensions = models.CharField(max_length=100, null=True)
    package_mass = MeasurementField(measurement=Mass, null=True)

    def __str__(self):
        return self.title
    
class User(AbstractUser):
    email = models.EmailField(max_length = 100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True)