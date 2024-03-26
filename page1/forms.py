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
from django.contrib.auth import authenticate
# from django_measurement.forms import MeasurementField, MeasurementWidget
from django_measurement.forms import MeasurementField, MeasurementWidget

from phonenumber_field.formfields import RegionalPhoneNumberWidget
from django.core.exceptions import ValidationError
from djmoney.forms.widgets import MoneyWidget

# from django_measurement.forms import MeasurementField, MeasurementWidget
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
            return [int(dim) if dim != 'x' else None for dim in value.split('x')]
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
        for dim in data_list:
            if dim is not None and dim < 0:
                raise ValidationError("Dimensions must be positive integers.")
        return f"{data_list[0] if data_list[0] is not None else 'x'}x{data_list[1] if data_list[1] is not None else 'x'}x{data_list[2] if data_list[2] is not None else 'x'}"

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
        }
        labels = {
            'nama_pt': 'Nama Perusahaan',
            'telp': 'No. Telpon',
            'npwp': 'NPWP',
        }
        choices = {
            'terms_of_payment': (('Cash', 'Cash'), ('Cash in Advance', 'Cash in Advance'), ('14 Hari', 'net 14 hari'), ('30 hari', 'net 30 hari'), ('45 hari', 'net 45 hari'),),
            'pengiriman': (('Soft Copy', 'Soft Copy'), ('Hard Copy', 'Hard Copy'), ('Keduanya', 'Keduanya')),
        }

    terms_of_payment = forms.ChoiceField(choices=Meta.choices['terms_of_payment'], widget=forms.Select(attrs={'class': 'form-control'}), label='Terms of Payment')
    pengiriman = forms.ChoiceField(choices=Meta.choices['pengiriman'], widget=forms.Select(attrs={'class': 'form-control'}), label='Pengiriman Faktur dan Invoice')

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
        }
        labels = {
            'nama_pt': 'Nama Perusahaan',
            'telp': 'No. Telpon',
            'npwp': 'NPWP',
        }
        choices = {
            'terms_of_payment': (('Cash', 'Cash'), ('Cash in Advance', 'Cash in Advance'), ('14 Hari', 'net 14 hari'), ('30 hari', 'net 30 hari'), ('45 hari', 'net 45 hari'),),
            'pengiriman': (('Soft Copy', 'Soft Copy'), ('Hard Copy', 'Hard Copy'), ('Keduanya', 'Keduanya')),
        }

    terms_of_payment = forms.ChoiceField(choices=Meta.choices['terms_of_payment'], widget=forms.Select(attrs={'class': 'form-control'}), label='Terms of Payment')
    pengiriman = forms.ChoiceField(choices=Meta.choices['pengiriman'], widget=forms.Select(attrs={'class': 'form-control'}), label='Pengiriman Faktur dan Invoice')


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
        exclude = ['SKU', 'gambar_resized', 'is_approved','upload_type']
        widgets = {
            'customer' : Select2Widget(attrs={'class':'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Baterai AA'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1, 2, 3, ...'}),
            'price': MoneyWidget(attrs={'class': 'form-control', 'placeholder': '100000'}),
            'gambar': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'category': Select2Widget(attrs={'class': 'form-control'}),
            'Tanggal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control','required': False}),
            'catatan': forms.Textarea(attrs={'class': 'form-control', 'placeholder':"Masukkan Spesifikasi Barang"}),
        }
        labels = {
            'customer':'Customer',
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
    unit = forms.ChoiceField(choices=Meta.choices['unit'], widget=Select2Widget(attrs={'class': 'form-control'}))


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
            'customer': Select2Widget(attrs={'class': 'form-control'}),
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
        # role = self.cleaned_data['role']
        # group = Group.objects.get(name=role)
        if commit:
            user.save()
            # user.groups.add(group)
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
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Add your custom authentication logic here
            user = authenticate(username =email, password=password)

            if user is None:
                raise forms.ValidationError(
                    _("Invalid email or password. Please try again.")
                )

        return cleaned_data

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = '__all__'
        exclude = ['id']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Judul'}),
            'package_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nama Paket'}),
            'messenger': Select2Widget(attrs={'class':'form-control'}),
            'vehicle': Select2Widget(attrs={'class':'form-control'}),
            'start_location': Select2Widget(attrs={'class': 'form-control'}),
            'destination': Select2Widget(attrs={'class': 'form-control'}),
            'start' : widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control', 'placeholder': 'Jam Keberangkatan'}),
            'end' : widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control', 'placeholder': 'Jam Kedatangan'}),
            'package_dimensions' : DimensionsInput(attrs={'class':'form-control'}),
        }
        labels = {
            'title' : 'Judul',
            'package_name' : 'Nama Paket',
            'messenger' : 'Pengantar',
            'vehicle' : 'Kendaraan',
            'start' : 'Jam Keberangkatan',
            'end' : 'Jam Kedatangan',
            'package_mass' : 'Berat Paket',
            'package_dimensions' : 'Dimensi Paket (p x l x t)',
        }
    package_mass = MeasurementField(
        measurement=Mass,
        unit_choices=(("kg","kg"), ("g","g")),
        widget = MeasurementWidget(attrs={'class':'form-control', 'placeholder':'10'}, unit_choices=(("kg","kg"), ("g","g"))),
    )
    package_dimensions = DimensionsField()

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

class LogBookForm(forms.ModelForm):
    class Meta:
        model = LogBook
        fields = ['nama', 'instansi_asal', 'email','telp', 'tujuan', 'tujuan_lainnya', 'start','end','nama_dikunjungi']
        widgets = {
            'nama': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nama Pengunjung'}),
            'instansi_asal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Institusi/Perusahaan'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'contoh@abc.com'}),
            'telp': RegionalPhoneNumberWidget(region='ID', attrs={'class': 'form-control', 'placeholder': '081-234-567-890'}),
            'tujuan':forms.Select(attrs={'class': 'form-control'}),
            'start' : widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control', 'placeholder': 'Jam Mulai Kunjungan'}),
            'end' : widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class':'form-control', 'placeholder': 'Jam Selesai Kunjungan'}),
            'nama_dikunjungi' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nama Yang Dikunjungi'}),
            'tujuan_lainnya': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nama': 'Nama Pengunjung',
            'instansi_asal': 'Institusi/Pengunjung Asal',
            'email': 'Email',
            'telp': 'No. Telpon',
            'tujuan': 'Tujuan Kunjungan',
            'start' : 'Jam Mulai',
            'end' : 'Jam Selesai',
            'nama_dikunjungi' : 'Nama Yang Dikunjungi',
            'tujuan_lainnya': 'Lainnya',
        }
        required = {
            'tujuan_lainnya': False,  # Set tujuan_lainnya as not required
        }

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()

class AdditionalAddressForm(forms.ModelForm):
    class Meta:
        model=DeliveryAddresses
        fields = '__all__'
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