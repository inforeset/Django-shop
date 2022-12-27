from unittest import TestCase
from django.forms import HiddenInput
from ..forms import CartAddProductForm


class CartAddProductFormTest(TestCase):

    def test_cart_add_product_form(self):
        form = CartAddProductForm()
        self.assertFalse(form.fields['quantity'].label)
        self.assertTrue(form.fields['update'].widget.__class__.__name__ == HiddenInput().__class__.__name__)
