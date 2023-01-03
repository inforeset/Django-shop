from django.test import TestCase
from django.urls import reverse


class ServicePaymentTest(TestCase):

    def test_get_right_response(self):
        response = self.client.post(reverse('pay_new'), {'card_number': 88888888})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(1, result['code'])

    def test_get_response_with_odd_card_number(self):
        response = self.client.post(reverse('pay_new'), {'card_number': 88888887})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(2, result['code'])

    def test_get_response_with_zero_in_the_the_end_of_card_number(self):
        response = self.client.post(reverse('pay_new'), {'card_number': 88888880})
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(2, result['code'])

    def test_service_accept_only_post(self):
        response = self.client.get(reverse('pay_new'), {'card_number': 88888880})
        self.assertEqual(response.status_code, 405)
