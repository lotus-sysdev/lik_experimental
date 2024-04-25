import datetime
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from django.core.validators import MaxValueValidator
from django_measurement.models import MeasurementField
from measurement.measures import Mass

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    nama_pt = models.CharField(max_length=255)
    telp = PhoneNumberField()
    terms_of_payment = models.CharField(max_length=15)
    pengiriman = models.CharField(max_length=50)
    npwp = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.cust_id:  # Generate cust_id only if it's not set
            current_year = timezone.now().year % 100  # Get the last two digits of the year
            last_customer = Customer.objects.filter(cust_id__gte=current_year*10000).order_by('-cust_id').first()
            if last_customer:
                last_id = last_customer.cust_id
                last_year = last_id // 10000  # Extract the year part from the cust_id
                if last_year == current_year:  # If it's the same year, increment the sequence
                    new_id = last_id + 1
                    if new_id % 10000 == 0:  # Check if the new_id has exceeded 9999
                        new_id = current_year * 100000 + 1  # Increment a zero in front of it
                else:  # If it's a new year, start the sequence from '0001'
                    new_id = current_year * 10000 + 1
            else:
                new_id = current_year * 10000 + 1
            self.cust_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_pt

class Supplier(models.Model):
    supp_id = models.AutoField(primary_key = True)
    nama_pt = models.CharField(max_length=255)
    telp = PhoneNumberField()
    terms_of_payment = models.CharField(max_length=50)
    pengiriman = models.CharField(max_length=50, null=True)
    npwp = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.supp_id: 
            current_year = timezone.now().year % 100  
            last_supplier = Supplier.objects.filter(supp_id__gte=current_year*10000).order_by('-supp_id').first()
            if last_supplier:
                last_id = last_supplier.supp_id
                last_year = last_id // 10000  # Extract the year part from the cust_id
                if last_year == current_year:  # If it's the same year, increment the sequence
                    new_id = last_id + 1
                    if new_id % 10000 == 0:  # Check if the new_id has exceeded 9999
                        new_id = current_year * 100000 + 1  # Increment a zero in front of it
                else:  # If it's a new year, start the sequence from '0001'
                    new_id = current_year * 10000 + 1
            else:
                new_id = current_year * 10000 + 1
            self.supp_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nama_pt

class CustomerPIC(models.Model):
    class Meta:
        verbose_name = "Customer PIC"
        verbose_name_plural = "Customer PICs"

    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    telp = PhoneNumberField()
    Role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nama}"

class SupplierPIC(models.Model):
    class Meta:
        verbose_name = "Supplier PIC"
        verbose_name_plural = "Supplier PICs"

    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    email = models.EmailField()
    telp = PhoneNumberField()
    Role = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.customer_id.nama_pt}-{self.nama}"

class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Items(models.Model):
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    SKU = models.CharField(max_length=20, primary_key = True, unique = True)
    upload_type = models.CharField(max_length=10, default = "manual")
    Tanggal = models.DateField(default=timezone.now)
    tanggal_pemesanan = models.DateField(default=timezone.now, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    pic = models.ForeignKey(CustomerPIC, on_delete= models.SET_NULL, null=True)
    nama = models.CharField(max_length=255)
    catatan = models.CharField(max_length = 500, null = True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10)
    price = MoneyField(max_digits=15, decimal_places=2, default_currency='IDR', blank= False, null= False, validators=[MinMoneyValidator(0)])
    gambar = models.ImageField(max_length=500)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nama
    
    def save(self, *args, **kwargs):
        if not self.SKU or 'is_approved' in kwargs:
            # Generate SKU based on category and a unique number
            if self.category and 'is_approved' not in kwargs:
                category_id_str = str(self.category.pk).zfill(2)  # Use the category ID, padded with a leading zero if needed
                category_code = self.category.name[:3].upper()  # Take the first three letters of the category

                # Retrieve the last SKU in the same category
                last_sku = Items.objects.filter(category=self.category).order_by('-SKU').first()

                if last_sku and last_sku.SKU:
                    last_number_str = str(last_sku.SKU)[5:9]  # Extract the number part of the SKU
                    if last_number_str.isdigit():
                        last_number = int(last_number_str)
                    else:
                        last_number = 0
                else:
                    last_number = 0

                # Format the current date as ddmmyy
                current_date = self.Tanggal.strftime('%y%m%d')

                new_sku = f"{category_id_str}{category_code}{last_number + 1:04d}{current_date}"  # Combine category ID, category code, a 4-digit number, and the formatted date
                self.SKU = new_sku

        super().save(*args, **kwargs)
        
class ItemSumber(models.Model):
    class Meta:
        verbose_name = "Item Sumber"
        verbose_name_plural = "Items Sources"

    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('Online Store', 'Online Store'),
        ('Rabrik', 'Pabrik'),
        ('Reseller', 'Reseller'),
        ('Grosir', 'Grosir'),
    )
    jenis_sumber = models.CharField(max_length=30, choices=TYPE_CHOICES)
    nama_perusahaan = models.CharField(max_length=255)
    telp = PhoneNumberField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    
class ItemChangeLog(models.Model):
    class Meta:
        verbose_name = "Item Change Log"
        verbose_name_plural = "Item Change Logs"

    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_changed = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)

class Provinsi(models.Model):
    class Meta:
        verbose_name = "Provinsi"
        verbose_name_plural = "Provinsi"
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Kota(models.Model):
    class Meta:
        verbose_name = "Kota/Kabupaten"
        verbose_name_plural = "Kota/Kabupaten"
    id = models.IntegerField(primary_key=True)
    provinsi_id = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name 
    
class Kecamatan(models.Model):
    class Meta:
        verbose_name = "Kecamatan"
        verbose_name_plural = "Kecamatan"
    id = models.IntegerField(primary_key=True)
    kota_id = models.ForeignKey(Kota, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name  
    
class Kelurahan(models.Model):
    class Meta:
        verbose_name = "Kelurahan/Desa"
        verbose_name_plural = "Kelurahan/Desa"
    id = models.IntegerField(primary_key=True)
    kecamatan_id = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class KodePos(models.Model):
    class Meta:
        verbose_name = "Kode Pos"
        verbose_name_plural = "Kode Pos"
    kode_pos = models.IntegerField()
    kelurahan_id = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.kode_pos)
    
class CustomerAlamat(models.Model):
    class Meta:
        verbose_name = "Customer Address"
        verbose_name_plural = "Customer Addresses"

    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('penagihan', 'Alamat Penagihan'),
        ('pengiriman', 'Alamat Pengiriman'),
    )
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    kode_pos = models.IntegerField (blank=True, null=True, validators=[MaxValueValidator(99999)])
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    detail = models.CharField(max_length=500)

    def __str__ (self):
        return (f'{self.customer_id}-{self.type}') 

class SupplierAlamat(models.Model):
    class Meta:
        verbose_name = "Supplier Address"
        verbose_name_plural = "Supplier Addresses"

    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    TYPE_CHOICES = (
        ('penagihan', 'Alamat Penagihan'),
        ('pengiriman', 'Alamat Pengiriman'),
    )
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    kode_pos = models.IntegerField (blank=True, null=True, validators=[MaxValueValidator(99999)])
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    detail = models.CharField(max_length=500)

    def __str__ (self):
        return (f'{self.supplier_id}-{self.type}') 

def default_date():
    return datetime.date(1900, 1, 1)

class PurchaseOrder(models.Model):
    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"

    supplier= models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    revenue_PO = MoneyField(max_digits=15, default_currency='IDR', blank=True, null=True, validators=[MinMoneyValidator(0)])
    nomor_PO = models.IntegerField(blank=True, null=True,)
    tanggal_PO = models.DateField(blank=True, null=True, )
    tanggal_process = models.DateField(blank=True, null=True, )
    tanggal_input_accurate = models.DateField(blank=True, null=True,)
    tanggal_pengiriman_barang = models.DateField(blank=True, null=True, )
    tanggal_pengiriman_invoice = models.DateField(blank=True, null=True, )
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
    class Meta:
        verbose_name = "Work Order"
        verbose_name_plural = "Work Orders"

    customer= models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    revenue_PO = MoneyField(max_digits=15, default_currency='IDR', blank=True, null=True, validators=[MinMoneyValidator(0)])
    nomor_PO = models.IntegerField(blank=True, null=True)
    tanggal_PO = models.DateField(blank=True, null=True)
    tanggal_process = models.DateField(blank=True, null=True)
    tanggal_input_accurate = models.DateField(blank=True, null=True)
    tanggal_pengiriman_barang = models.DateField(blank=True, null=True)
    tanggal_pengiriman_invoice = models.DateField(blank=True, null=True)
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
    class Meta:
        verbose_name = "User Action Log"
        verbose_name_plural = "User Action Logs"

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
    jenis = models.CharField(choices = JENIS_CHOICES, max_length=20)
    nomor_plat = models.CharField(max_length = 11)
    messenger = models.ForeignKey(Messenger, on_delete=models.SET_NULL, null=True, related_name='vehicles')

    def __str__(self):
        return self.nomor_plat

class DeliveryAddresses(models.Model):
    class Meta:
        verbose_name = "Delivery Address"
        verbose_name_plural = "Delivery Addresses"

    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    kode_pos = models.IntegerField (blank=True, null=True, validators=[MaxValueValidator(99999)])
    detail = models.CharField(max_length=500)
    
    def __str__(self):
        return self.detail

class Events(models.Model):
    class Meta:
        verbose_name = "Delivery Order"
        verbose_name_plural = "Delivery Orders"

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, null = True)
    start = models.DateTimeField(null = True, blank = True)
    end = models.DateTimeField(null = True, blank = True)
    messenger = models.ForeignKey(Messenger,on_delete=models.SET_NULL, null=True)
    keterangan = models.CharField(max_length = 500, null=True)
    start_location = models.ForeignKey(DeliveryAddresses, related_name= "delivery_start_location", on_delete=models.CASCADE, null =True)
    destination = models.ForeignKey(DeliveryAddresses, related_name="delivery_destination",on_delete=models.CASCADE, null =True)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.SET_NULL, null=True)
    package_name = models.CharField(max_length=100, null=True)
    package_dimensions = models.CharField(max_length=100, null=True)
    package_mass = MeasurementField(measurement=Mass, null=True)

    def __str__(self):
        return self.title

class LogBook(models.Model):
    class Meta:
        verbose_name = "Log Book"
        verbose_name_plural = "Log Books"

    id = models.AutoField(primary_key=True)
    instansi_asal = models.CharField(max_length = 255, null = True)
    nama = models.CharField(max_length=50, null = True)
    email = models.EmailField(max_length = 100)
    TUJUAN_CHOICES = (
        ("meeting", "Meeting"),
        ("survey", "Survey"),
        ("interview","Interview"),
        ("lainnya","Lainnya"),
    )
    tujuan = models.CharField(max_length = 20, null = True,choices = TUJUAN_CHOICES)
    tujuan_lainnya = models.CharField(max_length = 200, null = True, blank = True)
    nama_dikunjungi = models.CharField(max_length = 50, null=True)
    JENIS_CHOICES = (
        ("unscheduled", "Unscheduled"),
        ("scheduled", "Scheduled"),
    )
    tipe = models.CharField(max_length = 15, choices = JENIS_CHOICES)
    start = models.DateTimeField(null = True, blank = True)
    end = models.DateTimeField(null = True, blank = True)
    telp = PhoneNumberField()

    def __str__(self):
        return f"{self.title} ({self.start.strftime('%Y-%m-%d') if self.start else 'No start date'})"

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    employeeId = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    join_date = models.DateField()
    no_telp = PhoneNumberField()
    gender = models.CharField(max_length=10)
    status = models.CharField(max_length=100)
    tempat_lahir = models.CharField(max_length = 255)
    tanggal_lahir = models.DateField()
    no_ktp = models.BigIntegerField()
    no_rek = models.BigIntegerField()

class EmployeeAlamat(models.Model):
    class Meta:
        verbose_name = "Employee Address"
        verbose_name_plural = "Employee Addresses"
    
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    kode_pos = models.IntegerField (blank=True, null=True, validators=[MaxValueValidator(99999)])
    detail = models.CharField(max_length=500)

    def __str__ (self):
        return (f'{self.employee_id.name}') 


class Prospect(models.Model):
    prospect_id = models.AutoField(primary_key=True)
    tanggal = models.DateField(default=timezone.now)
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telp = PhoneNumberField() 
    in_charge = models.ForeignKey(User, on_delete=models.CASCADE)
    open = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nama} (Prospect)"
    
class ProspectLog(models.Model):
    class Meta:
        verbose_name = 'Prospect Log'
        verbose_name_plural = 'Prospect Logs'

    prospect_id = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)
    type = models.CharField(max_length=100) 
    activity = models.CharField(max_length=500)

class ProspectPIC(models.Model):
    class Meta:
        verbose_name = 'Prospect PIC'
        verbose_name_plural = 'Prospect PICs'

    prospect_id = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    telp = PhoneNumberField()
    Role  = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nama}"

class ProspectAddress(models.Model):
    class Meta:
        verbose_name = 'Prospect Address'
        verbose_name_plural = 'Prospect Addresses'

    prospect_id = models.ForeignKey(Prospect, on_delete=models.CASCADE)
    provinsi = models.ForeignKey(Provinsi, on_delete=models.CASCADE)
    kota = models.ForeignKey(Kota, on_delete=models.CASCADE)
    kecamatan = models.ForeignKey(Kecamatan, on_delete=models.CASCADE)
    kelurahan = models.ForeignKey(Kelurahan, on_delete=models.CASCADE)
    kode_pos = models.IntegerField (blank=True, null=True, validators=[MaxValueValidator(99999)])
    detail = models.CharField(max_length=500)


class User(AbstractUser):
    email = models.EmailField(max_length = 100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_set', blank=True)
