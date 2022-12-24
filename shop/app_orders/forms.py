from django import forms
from django.forms import HiddenInput

from .models import Order


class OrderCreateForm(forms.ModelForm):
    address = forms.CharField(max_length=150, label="Адрес", required=True,
                              widget=forms.Textarea(attrs={'class': 'form-input',
                                                           'maxlength': '150',
                                                           'data-validate': 'require',
                                                           'autocomplete': 'address'}))
    city = forms.CharField(max_length=30, label="Город", required=True,
                           widget=forms.TextInput(attrs={'class': 'form-input',
                                                         'maxlength': '30',
                                                         'data-validate': 'require',
                                                         'autocomplete': 'city'}))
    card_number = forms.CharField(min_length=8, max_length=9, required=True, label='Номер карты',
                                  widget=forms.TextInput(attrs={'class': 'form-input',
                                                                'data-validate': 'requireCard'}))

    class Meta:
        model = Order
        fields = ['address', 'city', 'delivery_type', 'payment_type', 'card_number']
        widgets = {
            'delivery_type': forms.RadioSelect,
            'payment_type': forms.RadioSelect
        }


class OrderPaymentForm(forms.ModelForm):

    card_number = forms.CharField(min_length=8, max_length=9, required=True, label='Номер карты',
                                  widget=forms.TextInput(attrs={'class': 'form-input',
                                                                'data-validate': 'requireCard'}))

    class Meta:
        model = Order
        fields = ['payment_type', 'card_number']
        widgets = {
            'payment_type': forms.RadioSelect
        }
