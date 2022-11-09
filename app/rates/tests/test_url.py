from django.test import TestCase
from django.urls import reverse


class RatesURLTest(TestCase):
    def test_url_html_is_correct(self):
        url = reverse('rates:form_data')
        self.assertEqual(url, '/')

    def test_url_api_is_correct(self):
        url = reverse('rates:currency_rates_api_v1')
        self.assertEqual(url, '/api/v1/')
