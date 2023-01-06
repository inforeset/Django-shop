from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1,
                                  max_value=21,
                                  widget=forms.NumberInput(
                                      attrs={'class': 'Amount-input form-input', 'min': '1', 'max': '21', 'size': '2',
                                             'maxlength': '2'}), label='')
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
