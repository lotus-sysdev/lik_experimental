from django import forms
from .models import *


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['id']
        widgets = {
            'plat' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'BG 123 XY'}),
            'driver' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Driver'}),
            'PO' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YY/MM/XXXX'}),
            'DO' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'XXX XXX'}),
            'no_tiket' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'I1900 XXX XXX'}),
            'berat' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1000, 2000, ...'}),
            'tanggal' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reject' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100, 200, ...'})
        }
        labels = {
            'PO' : 'Nomor PO',
            'DO' : 'Nomor DO',
            'no_tiket' : 'No. Tiket',
            'berat' : 'Berat (kg)',
            'reject' : 'Reject (kg)'
        }