import re
from django import forms
from django.forms import widgets
from django_select2.forms import Select2Widget
from .models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget
from django.core.exceptions import ValidationError
from djmoney.forms.fields import MoneyField
from djmoney.forms.widgets import MoneyWidget

from django_measurement.forms import MeasurementField, MeasurementWidget
from measurement.measures import Mass


def validate_npwp(value):
    cleaned_value = re.sub(r'\D', '', value)

    # Check if the cleaned value is either 15 or 16 digits
    if len(cleaned_value) == 15 or len(cleaned_value) == 16:
        return cleaned_value
    else:
        raise ValidationError('Invalid NPWP format')

    
class CustomerForm(forms.ModelForm):
    
    nama_pt = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'PT. Lotus Lestari Raya'}),
        label='Nama Perusahaan'
    )
    
    telp = PhoneNumberField(
        region="ID",
        widget=RegionalPhoneNumberWidget(region='ID', attrs={'class':'form-control', 'placeholder':'081-234-567-890'}),
        label='No. Telpon'
    )
    
    # Define choices for terms_of_payment field
    TERMS_OF_PAYMENT_CHOICES = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    terms_of_payment = forms.ChoiceField(
        choices=TERMS_OF_PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Terms of Payment'
    )

    # Define choices for pengiriman field
    PENGIRIMAN_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )
    pengiriman = forms.ChoiceField(
        choices=PENGIRIMAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Pengiriman'
    )

    npwp = forms.CharField(
        max_length=21,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'xx.xxx.xxx.x-xxx.xxx or xxxx xxxx xxxx xxxx'}),
        label='NPWP',
        validators=[validate_npwp]
    )

    def clean_npwp(self):
        npwp = self.cleaned_data.get('npwp')
        clean_npwp = validate_npwp(npwp)
        if len(clean_npwp) == 15:
            formatted_npwp = f'{clean_npwp[:2]}.{clean_npwp[2:5]}.{clean_npwp[5:8]}.{clean_npwp[8]}-{clean_npwp[9:12]}.{clean_npwp[12:]}'
        else:
            formatted_npwp = f'{clean_npwp[:4]} {clean_npwp[4:8]} {clean_npwp[8:12]} {clean_npwp[12:]}'
        return formatted_npwp
    
    faktur = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
        label='Faktur Pajak',
        required=False
    )

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['cust_id']

class SupplierForm(forms.ModelForm):
    nama_pt = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'PT. Lotus Lestari Raya'}),
        label='Nama Perusahaan'
    )
    
    telp = PhoneNumberField(
        region="ID",
        widget=RegionalPhoneNumberWidget(region='ID', attrs={'class':'form-control', 'placeholder':'081-234-567-890'}),
        label='No. Telpon'
    )
    
    # Define choices for terms_of_payment field
    TERMS_OF_PAYMENT_CHOICES = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    terms_of_payment = forms.ChoiceField(
        choices=TERMS_OF_PAYMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Terms of Payment'
    )

    npwp = forms.CharField(
        max_length=21,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'xx.xxx.xxx.x-xxx.xxx or xxxx xxxx xxxx xxxx'}),
        label='NPWP',
        validators=[validate_npwp]
    )
    
    def clean_npwp(self):
        npwp = self.cleaned_data.get('npwp')
        clean_npwp = validate_npwp(npwp)
        if len(clean_npwp) == 15:
            formatted_npwp = f'{clean_npwp[:2]}.{clean_npwp[2:5]}.{clean_npwp[5:8]}.{clean_npwp[8]}-{clean_npwp[9:12]}.{clean_npwp[12:]}'
        else:
            formatted_npwp = f'{clean_npwp[:4]} {clean_npwp[4:8]} {clean_npwp[8:12]} {clean_npwp[12:]}'
        return formatted_npwp    
    
    faktur = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-control'}),
        label='Faktur Pajak',
        required=False
    )

    class Meta:
        model = Supplier
        fields = '__all__'
        exclude=['supp_id']

class CustPICForms(forms.ModelForm):
    nama = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nama'}),
        label='Nama'
    )
    
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'username@lotuslestari.co.id'})
    )

    telp = PhoneNumberField(
        region="ID",
        widget=RegionalPhoneNumberWidget(region='ID', attrs={'class':'form-control', 'placeholder':'081-234-567-890'}),
        label='No. Telpon'
    )

    Role_Options = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    Role = forms.ChoiceField(
        choices=Role_Options,
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Jabatan'
    )

    class Meta:
        model = CustomerPIC
        fields = '__all__'
        exclude = ['customer_id']

class SuppPICForms(forms.ModelForm):
    nama = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nama'}),
        label='Nama'
    )
    
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'username@lotuslestari.co.id'})
    )

    telp = PhoneNumberField(
        region="ID",
        widget=RegionalPhoneNumberWidget(region='ID', attrs={'class':'form-control', 'placeholder':'081-234-567-890'}),
        label='No. Telpon'
    )

    Role_Options = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    Role = forms.ChoiceField(
        choices=Role_Options,
        widget=forms.Select(attrs={'class':'form-control'}),
        label='Jabatan'
    )

    class Meta:
        model = SupplierPIC
        fields = '__all__'
        exclude = ['supplier_id']

class CustAlamatForms(forms.ModelForm):
    TYPE_CHOICES = (
        ('penagihan', 'Alamat Penagihan'),
        ('pengiriman', 'Alamat Pengiriman'),
    )

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Jenis Alamat'
    )

    provinsi = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'DKI Jakarta'}),
        label='Provinsi'
    )

    kota = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Jakarta Barat'}),
        label='Kota'
    )

    kecamatan = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Kembangan'}),
        label='Nama Perusahaan'
    )

    kelurahan = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Srengseng'}),
        label='Nama Perusahaan'
    )

    detail = forms.CharField(
        max_length=255, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Ruko, Jl. Permata Regency Jl. H. Kelik No.31 Blok C, RT.1/RW.6,'}),
        label='Alamat Detail'
    )

    class Meta:
        model = CustomerAlamat
        fields = '__all__'
        exclude = ['customer_id']

class SuppAlamattForms(forms.ModelForm):
    TYPE_CHOICES = (
        ('penagihan', 'Alamat Penagihan'),
        ('pengiriman', 'Alamat Pengiriman'),
    )

    type = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Jenis Alamat'
    )

    provinsi = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'DKI Jakarta'}),
        label='Provinsi'
    )

    kota = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Jakarta Barat'}),
        label='Kota'
    )

    kecamatan = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Kembangan'}),
        label='Nama Perusahaan'
    )

    kelurahan = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Srengseng'}),
        label='Nama Perusahaan'
    )

    detail = forms.CharField(
        max_length=255, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Ruko, Jl. Permata Regency Jl. H. Kelik No.31 Blok C, RT.1/RW.6,'}),
        label='Alamat Detail'
    )

    class Meta:
        model = SupplierAlamat
        fields = '__all__'
        exclude = ['supplier_id']

class ItemForm(forms.ModelForm):
    nama = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Baterai AA'}),
        label='Nama Barang'
    )

    quantity = forms.CharField(
        max_length=255, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'1, 2, 3, ...'}),
        label='Kuantitas'
    )

    UNIT_CHOICES = (
        ('Botol', 'Botol'),
        ('Box', 'Box'),
        ('Bulan', 'Bulan'),
        ('Dirigen', 'Dirigen'),
        ('Item', 'Item'),
        ('Kaleng', 'Kaleng'),
        ('Kg', 'Kg'),
        ('Lusin', 'Lusin'),
        ('Meter', 'Meter'),
        ('Orang', 'Orang'),
        ('Pack', 'Pack'),
        ('Pail', 'Pail(Cat)'),
        ('Pair', 'Pair'),
        ('Pcs', 'Pcs'),
        ('Unit', 'Unit')
    )

    unit = forms.ChoiceField(
        choices=UNIT_CHOICES,
        widget=Select2Widget(attrs={'class':'form-control', 'placeholder':'Select unit of measurement'}),
        label=('Satuan')
    )

    price = MoneyField( 
        widget=MoneyWidget(attrs={'class': 'form-control', 'placeholder':'100000'}),
        label='Harga'
    )
    
    gambar = forms.FileField( 
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept':'image/*'}),
        label='Gambar',
        # validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    class Meta:
        model = Items
        fields = '__all__'
        exclude = ['SKU','gambar_resized', 'is_approved']
        widgets = {
            'category': Select2Widget(attrs={'class':'form-control'}),
        }
        labels = {
            'category': "Kategori",
        }

class SumberForm(forms.ModelForm):
    TYPE_CHOICES = (
        ('online', 'Online Store'),
        ('pabrik', 'Pabrik'),
    )
    jenis_sumber = forms.ChoiceField(
        choices=TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Jenis Sumber'
    )

    nama_perusahaan = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'PT. Lotus Lestari Raya'}),
        label='Nama Perusahaan'
    )

    telp = PhoneNumberField(
        region="ID",
        widget=RegionalPhoneNumberWidget(region='ID', attrs={'class':'form-control', 'placeholder':'081-234-567-890'}),
        label='No. Telpon'
    )

    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'username@lotuslestari.co.id'})
    )

    url = forms.URLField(
        widget=forms.URLInput(attrs={'class':'form-control', 'placeholder':'https://beezywork.id'}),
    )

    class Meta:
        model = ItemSumber
        fields = '__all__'
        exclude = ['item']

class PurchaseForm(forms.ModelForm):
    revenue_PO = MoneyField( 
        required=False,
        widget=MoneyWidget(attrs={'class': 'form-control', 'placeholder':'100000'}),
        label='Revenue PO'
    )
    
    nomor_PO = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        label=('Nomor PO')
    )
    
    tanggal_PO = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label=('Tanggal PO')
    )
    
    tanggal_process = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label=("Tanggal Proses")
    )
    
    tanggal_input_accurate = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label=("Tanggal input Accurate")
    )
    
    tanggal_pengiriman_barang = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'})
    )
    
    tanggal_pengiriman_invoice = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'})
    )

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        exclude = ['status']
        widgets = {
            'supplier': Select2Widget(attrs={'class':'form-control'}),
            'item': Select2Widget(attrs={'class':'form-control'}),
        }

class WorkForm(forms.ModelForm):
    revenue_PO = MoneyField( 
        required=False,
        widget=MoneyWidget(attrs={'class': 'form-control', 'placeholder':'100000'}),
        label='Revenue PO'
    )
    
    nomor_PO = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class':'form-control'}),
        label=('Nomor PO')
    )
    
    tanggal_PO = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label=('Tanggal PO')
    )
    
    tanggal_process = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label=("Tanggal Proses")
    )
    
    tanggal_input_accurate = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        label=("Tanggal input Accurate")
    )
    
    tanggal_pengiriman_barang = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'})
    )
    
    tanggal_pengiriman_invoice = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control'})
    )

    class Meta:
        model = WorkOrder
        fields = "__all__"
        exclude = ['status']
        widgets = {
            'customer': Select2Widget(attrs={'class':'form-control'}),
            'item': Select2Widget(attrs={'class':'form-control'}),
        }

class Register(UserCreationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={'class':'form-control'}),
        error_messages= {'required': 'Please enter a username.'},
    )

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class':'form-control'}),
        error_messages= {'required': 'Please provide your email address.'},
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),
        error_messages={'required': 'Please enter your password.'}
    )
    password2 = forms.CharField(
        label='Password confirmation',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}),
        error_messages={'required': 'Please confirm your password.'}
    )

    Role_Choices = (
        ('GA','General Affairs'),
        ('Accounting','Accounting')
    )
    role = forms.ChoiceField(
        choices=Role_Choices,
        label='Role',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('The passwords do not match.')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data['role']
        group = Group.objects.get(name=role)
        if commit:
            user.save()
            user.groups.add(group)
        return user

class Login(AuthenticationForm):
    email = forms.EmailField(
        required=True,
        label=_("Email"),
        widget=forms.EmailInput(attrs={'autofocus': True}),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)
        self.fields['email'].widget.attrs.update({'class':'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

class DeliveryForm(forms.ModelForm):
    title = forms.CharField(
        max_length=30,
        label='Judul',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Judul'}),
    )
    start = forms.DateTimeField(
        label='Jam Keberangkatan', 
        widget=widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control', 'placeholder': 'Jam Keberangkatan'})
        )
    end = forms.DateTimeField(
        label='Jam Kedatangan', 
        widget=widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control', 'placeholder': 'Jam Kedatangan'})
        )
    DESTINATION_CHOICES = (
        ('beezy', 'Beezy Work'),
        ('dest1', 'Dest 1'),
    )
    start_location = forms.ChoiceField(
        choices = DESTINATION_CHOICES,
        label= "Lokasi Keberangkatan",
        widget= forms.Select(attrs={'class':'form-control'})
        )
    destination =  forms.ChoiceField(
        choices = DESTINATION_CHOICES,
        label= "Destinasi",
        widget= forms.Select(attrs={'class':'form-control'})
        )

    package_name = forms.CharField(
        max_length=30,
        label= "Nama Paket",
        widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder': 'Nama Paket'})
    )
    package_dimensions = forms.CharField(
        max_length=30,
        label= "Dimensi Paket",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'panjang x lebar x tinggi'})
    )
    package_mass = MeasurementField(
        measurement=Mass,
        unit_choices=(("kg","kg"), ("g","g")),
        label="Berat Paket",
        widget = MeasurementWidget(attrs={'class':'form-control', 'placeholder':'10'}, unit_choices=(("kg","kg"), ("g","g")))
    )
    class Meta:
        model = Events
        fields = '__all__'
        exclude = ['id']
        widgets = {
            'messenger': Select2Widget(attrs={'class':'form-control'}),
            'vehicle': Select2Widget(attrs={'class':'form-control'}),
        }
        labels = {
            'messenger' : 'Pengantar',
            'vehicle' : 'Kendaraan',
        }

class MessengerForm(forms.ModelForm):
    class Meta:
        model = Messenger
        fields = '__all__'
        exclude = ['id']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        exclude = ['id']