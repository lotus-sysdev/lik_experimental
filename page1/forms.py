import re
from django import forms
from django.forms import widgets
from django_select2.forms import Select2Widget
from .models import *

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget
from django.core.exceptions import ValidationError
from djmoney.forms.fields import MoneyField
from djmoney.forms.widgets import MoneyWidget

from django_measurement.forms import MeasurementField, MeasurementWidget
from measurement.measures import Mass

class DimensionsInput(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs={'class':'form-control', 'style':'width:33%', 'placeholder': 'Panjang (cm)'}),
            forms.NumberInput(attrs={'class':'form-control', 'style':'width:33%', 'placeholder': 'Lebar (cm)'}),
            forms.NumberInput(attrs={'class':'form-control', 'style':'width:33%', 'placeholder': 'Tinggi (cm)'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [int(dim) for dim in value.split('x')]
        return [None, None, None]

class DimensionsField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
            forms.IntegerField(),
        )
        super().__init__(fields, *args, **kwargs)
        self.widget = DimensionsInput() 

    def compress(self, data_list):
        return f"{data_list[0]}x{data_list[1]}x{data_list[2]}"

def validate_npwp(value):
    cleaned_value = re.sub(r'\D', '', value)

    # Check if the cleaned value is either 15 or 16 digits
    if len(cleaned_value) == 15 or len(cleaned_value) == 16:
        return cleaned_value
    else:
        raise ValidationError('Invalid NPWP format')

class CustomerForm(forms.ModelForm):

    def clean_npwp(self):
        npwp = self.cleaned_data.get('npwp')
        clean_npwp = validate_npwp(npwp)
        if len(clean_npwp) == 15:
            formatted_npwp = f'{clean_npwp[:2]}.{clean_npwp[2:5]}.{clean_npwp[5:8]}.{clean_npwp[8]}-{clean_npwp[9:12]}.{clean_npwp[12:]}'
        else:
            formatted_npwp = f'{clean_npwp[:4]} {clean_npwp[4:8]} {clean_npwp[8:12]} {clean_npwp[12:]}'
        return formatted_npwp

    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['cust_id']
        widgets = {
            'nama_pt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PT. Lotus Lestari Raya'}),
            'telp': RegionalPhoneNumberWidget(region='ID', attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
            'npwp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'xx.xxx.xxx.x-xxx.xxx or xxxx xxxx xxxx xxxx'}),
            'faktur': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nama_pt': 'Nama Perusahaan',
            'telp': 'No. Telpon',
            'terms_of_payment': 'Terms of Payment',
            'pengiriman': 'Pengiriman',
            'npwp': 'NPWP',
            'faktur': 'Faktur Pajak',
        }
        choices = {
            'terms_of_payment': ((1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3')),
            'pengiriman': ((True, 'Yes'), (False, 'No')),
        }

    terms_of_payment = forms.ChoiceField(choices=Meta.choices['terms_of_payment'], widget=forms.Select(attrs={'class': 'form-control'}), label='Terms of Payment')
    pengiriman = forms.ChoiceField(choices=Meta.choices['pengiriman'], widget=forms.Select(attrs={'class': 'form-control'}), label='Pengiriman')

class SupplierForm(forms.ModelForm):
    def clean_npwp(self):
        npwp = self.cleaned_data.get('npwp')
        clean_npwp = validate_npwp(npwp)
        if len(clean_npwp) == 15:
            formatted_npwp = f'{clean_npwp[:2]}.{clean_npwp[2:5]}.{clean_npwp[5:8]}.{clean_npwp[8]}-{clean_npwp[9:12]}.{clean_npwp[12:]}'
        else:
            formatted_npwp = f'{clean_npwp[:4]} {clean_npwp[4:8]} {clean_npwp[8:12]} {clean_npwp[12:]}'
        return formatted_npwp

    class Meta:
        model = Supplier
        fields = '__all__'
        exclude = ['supp_id']
        widgets = {
            'nama_pt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PT. Lotus Lestari Raya'}),
            'telp': RegionalPhoneNumberWidget(region='ID', attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
            'npwp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'xx.xxx.xxx.x-xxx.xxx or xxxx xxxx xxxx xxxx'}),
            'faktur': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nama_pt': 'Nama Perusahaan',
            'telp': 'No. Telpon',
            'terms_of_payment': 'Terms of Payment',
            'npwp': 'NPWP',
            'faktur': 'Faktur Pajak',
        }
        choices = {
            'terms_of_payment': ((1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3')),
        }

    terms_of_payment = forms.ChoiceField(choices=Meta.choices['terms_of_payment'], widget=forms.Select(attrs={'class': 'form-control'}), label='Terms of Payment')

class CustPICForms(forms.ModelForm):
    class Meta:
        model = CustomerPIC
        fields = '__all__'
        exclude = ['customer_id']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username@lotuslestari.co.id'}),
            'telp': RegionalPhoneNumberWidget(region='ID', attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
        }
        labels = {
            'nama': 'Nama',
            'email': 'Email',
            'telp': 'No. Telpon',
        }
        choices = {
            'Role': (('Finance', 'Finance'), ('General Affairs', 'General Affairs (GA)'), ('Sales', 'Sales'), ('Procurement', 'Procurement'),('Board of Directors', 'Board of Directors (BOD)'),)
        }
    Role = forms.ChoiceField(choices=Meta.choices['Role'], widget=forms.Select(attrs={'class': 'form-control'}), label='Jabatan')

class SuppPICForms(forms.ModelForm):
    class Meta:
        model = SupplierPIC
        fields = '__all__'
        exclude = ['supplier_id']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username@lotuslestari.co.id'}),
            'telp': RegionalPhoneNumberWidget(region='ID', attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
        }
        labels = {
            'nama': 'Nama',
            'email': 'Email',
            'telp': 'No. Telpon',
        }
        choices = {
            'Role': (('Finance', 'Finance'), ('General Affairs', 'General Affairs (GA)'), ('Sales', 'Sales'), ('Procurement', 'Procurement'),('Board of Directors', 'Board of Directors (BOD)'),)
        }
    Role = forms.ChoiceField(choices=Meta.choices['Role'], widget=forms.Select(attrs={'class': 'form-control'}), label='Jabatan')

class CustAlamatForms(forms.ModelForm):
    class Meta:
        model = CustomerAlamat
        fields = '__all__'
        exclude = ['customer_id']
        widgets = {
            'provinsi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DKI Jakarta'}),
            'kota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jakarta Barat'}),
            'kecamatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kembangan'}),
            'kelurahan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Srengseng'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ruko, Jl. Permata Regency Jl. H. Kelik No.31 Blok C, RT.1/RW.6,'}),
        }
        labels = {
            'provinsi': 'Provinsi',
            'kota': 'Kota',
            'kecamatan': 'Kecamatan',
            'kelurahan': 'Kelurahan',
            'detail': 'Alamat Detail',
        }
        choices = {
            'type': (('penagihan', 'Alamat Penagihan'), ('pengiriman', 'Alamat Pengiriman'),)
        }
    type = forms.ChoiceField(choices=Meta.choices['type'], widget=forms.Select(attrs={'class': 'form-control'}), label='Jenis Alamat')

class SuppAlamattForms(forms.ModelForm):
    class Meta:
        model = SupplierAlamat
        fields = '__all__'
        exclude = ['supplier_id']
        widgets = {
            'provinsi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DKI Jakarta'}),
            'kota': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jakarta Barat'}),
            'kecamatan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kembangan'}),
            'kelurahan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Srengseng'}),
            'detail': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ruko, Jl. Permata Regency Jl. H. Kelik No.31 Blok C, RT.1/RW.6,'}),
        }
        labels = {
            'provinsi': 'Provinsi',
            'kota': 'Kota',
            'kecamatan': 'Kecamatan',
            'kelurahan': 'Kelurahan',
            'detail': 'Alamat Detail',
        }
        choices = {
            'type': (('penagihan', 'Alamat Penagihan'), ('pengiriman', 'Alamat Pengiriman'),)
        }
    type = forms.ChoiceField(choices=Meta.choices['type'], widget=forms.Select(attrs={'class': 'form-control'}), label='Jenis Alamat')

class ItemForm(forms.ModelForm):
    class Meta:
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
            ('Unit', 'Unit'),
            ('Lainnya', 'Lainnya')
        )

        model = Items
        fields = '__all__'
        exclude = ['SKU', 'gambar_resized', 'is_approved']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Baterai AA'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1, 2, 3, ...'}),
            'price': MoneyWidget(attrs={'class': 'form-control', 'placeholder': '100000'}),
            'gambar': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'category': Select2Widget(attrs={'class': 'form-control'}),
            'Tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'nama': 'Nama Barang',
            'quantity': 'Kuantitas',
            'unit': 'Satuan',
            'price': 'Harga',
            'gambar': 'Gambar',
            'category': 'Kategori',
            'Tanggal': 'Tanggal Input'
        }
        choices = {
            'unit': UNIT_CHOICES,
        }
    unit = forms.ChoiceField(choices=Meta.choices['unit'], widget=forms.Select(attrs={'class': 'form-control'}))

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise ValidationError('Kuantitas harus positif.')
        return quantity

class SumberForm(forms.ModelForm):
    class Meta:
        model = ItemSumber
        fields = '__all__'
        exclude = ['item']
        widgets = {
            'nama_perusahaan' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PT. Lotus Lestari Raya'}),
            'telp' : RegionalPhoneNumberWidget(attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
            'email' : forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'username@lotuslestari.co.id'}),
            'url' : forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://beezywork.id'}),
        }
        labels = {
            'jenis_sumber' : 'Jenis Sumber*',
            'nama_perusahaan' : 'Nama Perusahaan*',
            'telp' : 'No. Telpon',
            'email' : 'Email',
            'url' : 'Link',
        }
        choices = {
            'jenis_sumber': (('Online Store', 'Online Store'), ('Rabrik', 'Pabrik'), ('Reseller', 'Reseller'), ('Grosir', 'Grosir'),)
        }
        
    jenis_sumber = forms.ChoiceField(choices=Meta.choices['jenis_sumber'], widget=forms.Select(attrs={'class': 'form-control'}), label='Jenis Sumber*')

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        exclude = ['status']
        widgets = {
            'supplier': Select2Widget(attrs={'class': 'form-control'}),
            'item': Select2Widget(attrs={'class': 'form-control'}),
            'revenue_PO': MoneyWidget(attrs={'class': 'form-control', 'placeholder': '100000'}),
            'nomor_PO': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '012345'}),
            'tanggal_PO': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_process': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_input_accurate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_pengiriman_barang': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_pengiriman_invoice': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'revenue_PO': 'Revenue PO',
            'nomor_PO': 'Nomor PO',
            'tanggal_PO': 'Tanggal PO',
            'tanggal_process': 'Tanggal Proses',
            'tanggal_input_accurate': 'Tanggal Input Accurate',
            'tanggal_pengiriman_barang': 'Tanggal Pengiriman Barang',
            'tanggal_pengiriman_invoice': 'Tanggal Pengiriman Invoice',
        }

class PurchaseFormNGA(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ['tanggal_process', 'tanggal_input_accurate', 'tanggal_pengiriman_barang', 'tanggal_pengiriman_invoice']
        widgets = {
            'tanggal_process': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_input_accurate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_pengiriman_barang': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_pengiriman_invoice': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'tanggal_process': 'Tanggal Proses',
            'tanggal_input_accurate': 'Tanggal Input Accurate',
            'tanggal_pengiriman_barang': 'Tanggal Pengiriman Barang',
            'tanggal_pengiriman_invoice': 'Tanggal Pengiriman Invoice',
        }

class WorkForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = "__all__"
        exclude = ['status']
        widgets = {
            'supplier': Select2Widget(attrs={'class': 'form-control'}),
            'item': Select2Widget(attrs={'class': 'form-control'}),
            'revenue_PO': MoneyWidget(attrs={'class': 'form-control', 'placeholder': '100000'}),
            'nomor_PO': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '012345'}),
            'tanggal_PO': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_process': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_input_accurate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_pengiriman_barang': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_pengiriman_invoice': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'revenue_PO': 'Revenue PO',
            'nomor_PO': 'Nomor PO',
            'tanggal_PO': 'Tanggal PO',
            'tanggal_process': 'Tanggal Proses',
            'tanggal_input_accurate': 'Tanggal Input Accurate',
            'tanggal_pengiriman_barang': 'Tanggal Pengiriman Barang',
            'tanggal_pengiriman_invoice': 'Tanggal Pengiriman Invoice',
        }

class WorkFormNGA(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['tanggal_process', 'tanggal_input_accurate', 'tanggal_pengiriman_barang', 'tanggal_pengiriman_invoice']
        widgets = {
            'tanggal_process': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_input_accurate': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_pengiriman_barang': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tanggal_pengiriman_invoice': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
        labels = {
            'tanggal_process': 'Tanggal Proses',
            'tanggal_input_accurate': 'Tanggal Input Accurate',
            'tanggal_pengiriman_barang': 'Tanggal Pengiriman Barang',
            'tanggal_pengiriman_invoice': 'Tanggal Pengiriman Invoice',
        }

# TODO Validation for everything below this
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
        ('Accounting','Accounting'),
        ('Messenger', 'Messenger')
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
    package_dimensions = DimensionsField(
        label= "Dimensi Paket",
        widget=DimensionsInput(attrs={'class':'form-control'})
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