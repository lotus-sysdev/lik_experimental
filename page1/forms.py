from django import forms
from django_select2.forms import Select2Widget
from .models import *
# from django.core.validators import FileExtensionValidator

class CustomerForm(forms.ModelForm):
    nama_pt = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'PT. Lotus Lestari Raya'}),
        label='Nama Perusahaan'
    )
    
    telp = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'+628xxxxxxxxxx'}),
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
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'xx.xxx.xxx.x-xxx.xxx'}),
        label='NPWP'
    )
    
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
    
    telp = forms.CharField(
        max_length=15, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'+628xxxxxxxxxx'}),
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
        max_length=20,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'xx.xxx.xxx.x-xxx.xxx'}),
        label='NPWP'
    )
    
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
    Role_Options = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    Role = forms.ChoiceField(choices=Role_Options)

    class Meta:
        model = CustomerPIC
        fields = '__all__'
        exclude = ['customer_id']

class SuppPICForms(forms.ModelForm):
    Role_Options = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    Role = forms.ChoiceField(choices=Role_Options)

    class Meta:
        model = SupplierPIC
        fields = '__all__'
        exclude = ['supplier_id']

class CustAlamatForms(forms.ModelForm):
    class Meta:
        model = CustomerAlamat
        fields = '__all__'
        exclude = ['customer_id']

class SuppAlamattForms(forms.ModelForm):
    class Meta:
        model = SupplierAlamat
        fields = '__all__'
        exclude = ['supplier_id']

class ItemForm(forms.ModelForm):
    nama = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'PT. Lotus Lestari Raya'}),
        label='Nama Barang'
    )

    category = forms.CharField(
        max_length=255, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Office Supplies'}),
        label='Kategori'
    )

    quantity = forms.CharField(
        max_length=255, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'1, 2, 3, ...'}),
        label='Kuantitas'
    )

    price = forms.CharField(
        max_length=255, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'100000'}),
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
        exclude = ['SKU','gambar_resized']

class SumberForm(forms.ModelForm):

    class Meta:
        model = ItemSumber
        fields = '__all__'
        exclude = ['item']

class PurchaseForm(forms.ModelForm):
    tanggal_PO = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tanggal_process = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tanggal_input_accurate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tanggal_pengiriman_barang = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tanggal_pengiriman_invoice = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        exclude=['supplier_id','status']
        widgets = {
            'item': Select2Widget,
        }
class WorkForm(forms.ModelForm):

    class Meta:
        model = WorkOrder
        fields = '__all__'
        exclude=['supplier_id','item','status']