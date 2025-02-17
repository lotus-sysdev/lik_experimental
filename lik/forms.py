from django import forms
from django.forms import widgets
from django_select2.forms import Select2Widget
from .models import *

class ReportForm(forms.ModelForm):
    def clean_DO(self):
        do = str(self.cleaned_data['DO']).replace(" ", "")  # Convert to string
        if len(do) !=10:
            raise forms.ValidationError("Nomor DO harus terdiri dari 6 karakter.")
        # Add spaces in the appropriate positions
        return ' '.join([do[:5], do[5:]])

    def clean_no_tiket(self):
        no_tiket = str(self.cleaned_data['no_tiket']).replace(" ", "")
        # Add spaces in the appropriate positions
        return ' '.join([no_tiket[:5], no_tiket[5:8], no_tiket[8:]])
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['id']
        widgets = {
            'sender': Select2Widget(attrs={'class': 'form-control'}),
            'tiketId': forms.TextInput(attrs={'class': 'form-control', 'disabled' : 'disabled'}),
            'plat' : forms.TextInput(attrs={'class':'form-control', 'placeholder': 'BG 123 XY'}),
            'driver' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Driver'}),
            'PO' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YY/MM/XXXX'}),
            'DO' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXX XXX'}),
            'lokasi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lokasi Pemotongan'}),
            'tujuan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pabrik Tujuan'}),
            'kayu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Jenis Kayu'}),
            'no_tiket' : forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'I1900 XXX XXX'}),
            'berat' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1000, 2000, ...'}),
            'tanggal' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reject' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '100, 200, ...'}),
            'foto' : forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'og_foto' : forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'tiketId' : 'ID Tiket',
            'PO' : 'Nomor PO',
            'DO' : 'Nomor DO',
            'lokasi' : 'Lokasi Pemotongan',
            'tujuan' : 'Pabrik Tujuan',
            'kayu' : 'Jenis Kayu',
            'no_tiket' : 'No. Tiket',
            'berat' : 'Berat (kg)',
            'tanggal' : 'Tanggal Keluar',
            'reject' : 'Reject (kg)',
            'foto' : 'Thumbnail',
            'og_foto' : 'Submitted Photo',
        }
    date_time = forms.DateTimeField(
        widget=widgets.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control', 'placeholder': 'Timestamp'}),
        label='Timestamp',
        required=False,
        disabled=True
    )

class ReportFilterForm(forms.Form):
    sender = forms.ChoiceField(
        choices=[], 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    kayu = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    start_date = forms.DateField(
        label='Start Date', 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    end_date = forms.DateField(
        label='End Date', 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender'].choices = self.get_sender_choices()
        self.fields['kayu'].choices = self.get_kayu_choices()

    def get_sender_choices(self):
        sender_choices = [(sender["sender__username"], f"{sender['sender__first_name']}") for sender in Report.objects.values('sender__username', 'sender__first_name').distinct()]
        return [('', 'Select a Sender')] + sender_choices
    
    def get_kayu_choices(self):
        kayu_choices = [(kayu["kayu"], kayu["kayu"]) for kayu in Report.objects.values('kayu').distinct()]
        return [('', 'Select Jenis Kayu')] + kayu_choices

