from django.test import TestCase
from django.forms import Textarea, TextInput, RadioSelect
from app_orders.forms import OrderCreateForm


class OrderCreateFormTest(TestCase):

    def test_field_address_form(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['address'].label, 'Адрес')
        self.assertEqual(form.fields['address'].max_length, 150)
        self.assertTrue(form.fields['address'].required)
        self.assertTrue(form.fields['address'].widget.__class__.__name__ == Textarea().__class__.__name__)

    def test_field_city_form(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['city'].label, 'Город')
        self.assertEqual(form.fields['city'].max_length, 30)
        self.assertTrue(form.fields['city'].required)
        self.assertTrue(form.fields['city'].widget.__class__.__name__ == TextInput().__class__.__name__)

    def test_field_card_number_form(self):
        form = OrderCreateForm()
        self.assertEqual(form.fields['card_number'].label, 'Номер карты')
        self.assertEqual(form.fields['card_number'].max_length, 9)
        self.assertEqual(form.fields['card_number'].min_length, 8)
        self.assertTrue(form.fields['card_number'].required)
        self.assertTrue(form.fields['card_number'].widget.__class__.__name__ == TextInput().__class__.__name__)

    def test_field_delivery_type_form(self):
        form = OrderCreateForm()
        self.assertTrue(form.fields['delivery_type'].widget.__class__.__name__ == RadioSelect().__class__.__name__)

    def test_field_payment_type_form(self):
        form = OrderCreateForm()
        self.assertTrue(form.fields['payment_type'].widget.__class__.__name__ == RadioSelect().__class__.__name__)
