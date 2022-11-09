import datetime

from django.test import TestCase
from django.urls import resolve, reverse

from rates import models, views


class RatesViewTest(TestCase):
    def test_rates_view_function_isvalid(self):
        view = resolve('/')
        self.assertIs(view.func.view_class, views.DateValuesView)

    def test_rates_view_return_status_code_200(self):
        response = self.client.get(reverse('rates:form_data'))
        self.assertEqual(response.status_code, 200)

    def test_rates_view_return_correct_template(self):
        response = self.client.get(reverse('rates:form_data'))
        self.assertTemplateUsed(response, 'rates/pages/graphics.html')

    def test_rates_view_return_no_graphics_when_get(self):
        response = self.client.get(reverse('rates:form_data'))
        self.assertNotIn(
            '<script src="https://code.highcharts.com/highcharts.src.js">'
            '</script>',
            response.content.decode('utf-8')
        )


class RatesViewApiTest(TestCase):
    def setUp(self) -> None:
        self.date = datetime.datetime.strptime('2022-11-04', '%Y-%m-%d').date()
        models.CurrencyRate.objects.create(
            date=self.date,
            brl_rate=10,
            eur_rate=11,
            jpy_rate=12,
        )
        return super().setUp()

    def test_rates_api_v1(self):
        response = self.client.get(reverse('rates:currency_rates_api_v1'))
        self.assertEqual(
            response.content.decode('utf-8'),
            '[{"date": "2022-11-04", "brl_rate": 10.0, "eur_rate": 11.0,'
            ' "jpy_rate": 12.0}]'
        )
