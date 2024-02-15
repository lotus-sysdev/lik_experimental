from django import forms
from .models import Customer, PIC

class CustomerForm(forms.ModelForm):
    # Define choices for terms_of_payment field
    TERMS_OF_PAYMENT_CHOICES = (
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
    )
    terms_of_payment = forms.ChoiceField(choices=TERMS_OF_PAYMENT_CHOICES)

    # Define choices for pengiriman field
    PENGIRIMAN_CHOICES = (
        (True, 'Yes'),
        (False, 'No'),
    )
    pengiriman = forms.ChoiceField(choices=PENGIRIMAN_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = '__all__'
        exclude=['cust_id']

class PIC_Forms(forms.ModelForm):
    class Meta:
        model = PIC
        fields = '__all__'
        exclude = ['PIC_Id']



