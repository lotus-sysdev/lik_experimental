from django import forms
from .models import *


class ReportForm(forms.ModelForm):
    def clean_DO(self):
        do = str(self.cleaned_data['DO']).replace(" ", "")  # Convert to string
        if len(do) !=6:
            raise forms.ValidationError("Nomor DO harus terdiri dari 6 karakter.")
        # Add spaces in the appropriate positions
        return ' '.join([do[:3], do[3:]])

    def clean_no_tiket(self):
        no_tiket = str(self.cleaned_data['no_tiket']).replace(" ", "")
        # Add spaces in the appropriate positions
        return ' '.join([no_tiket[:4], no_tiket[4:7], no_tiket[7:]])
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['id']
        widgets = {
            'plat' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'BG 123 XY'}),
            'driver' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Driver'}),
            'PO' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YY/MM/XXXX'}),
            'DO' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX XXX'}),
            'no_tiket' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'I1900 XXX XXX'}),
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