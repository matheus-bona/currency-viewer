import datetime

from django.test import TestCase

from ..models import CurrencyRate
from ..tools.date_tools import DateTools
from ..tools.request_currency import Currency


class RequestCurrencyTest(TestCase, Currency):
    def test_rates_tool_get_currency_from_api(self):
        response = self.get_currency_from_api(
            date=datetime.datetime.strptime('2022-11-04', '%Y-%m-%d').date()
        )
        self.assertEqual(
            response,
            {
                'BRL': 5.032617504051864,
                'EUR': 1.012965964343598,
                'JPY': 147.072528363047
            }
        )

    def test_rates_tool_get_currency_from_api_wrong_url(self):

        response = self.get_currency_from_api(
            date=datetime.datetime.strptime(
                '2022-11-04', '%Y-%m-%d').date(),
            url='https://test123412345.com'
        )
        self.assertEqual(response, None)

    def test_rates_tool_get_currency_from_api_wrong_endpoint(self):

        response = self.get_currency_from_api(
            date=datetime.datetime.strptime(
                '2022-11-04', '%Y-%m-%d').date(),
            url='https://api.vatcomply.com/get404'
        )

        self.assertEqual(response, None)

    def test_rates_tool_get_range_currencies_from_api(self):
        date = datetime.datetime.strptime('2022-11-04', '%Y-%m-%d').date()
        currencyRate = CurrencyRate.objects.filter(date=date).first()
        self.assertEqual(currencyRate, None)

        data_list = self.get_range_currencies(range_date=[date])
        currencyRate_new = CurrencyRate.objects.filter(date=date).first()

        self.assertEqual(
            data_list[0].get('rates').get('BRL'),
            currencyRate_new.brl_rate
        )
        self.assertEqual(
            data_list[0].get('rates').get('EUR'),
            currencyRate_new.eur_rate
        )
        self.assertEqual(
            data_list[0].get('rates').get('JPY'),
            currencyRate_new.jpy_rate
        )

    def test_rates_tool_get_range_currencies_from_db(self):
        date = datetime.datetime.strptime('2022-11-04', '%Y-%m-%d').date()

        self.get_range_currencies(range_date=[date])
        currencyRate_new = CurrencyRate.objects.filter(date=date).first()

        data_list = self.get_range_currencies(range_date=[date])

        self.assertEqual(
            data_list[0].get('rates').get('BRL'),
            currencyRate_new.brl_rate
        )
        self.assertEqual(
            data_list[0].get('rates').get('EUR'),
            currencyRate_new.eur_rate
        )
        self.assertEqual(
            data_list[0].get('rates').get('JPY'),
            currencyRate_new.jpy_rate
        )


class DateToolsTest(TestCase, DateTools):
    def test_get_business_days_range_given_str(self):
        result = self.get_business_days_range(
            start_date='2022-11-04',
            end_date='2022-11-07'
        )
        self.assertEqual(
            result[0],
            datetime.datetime.strptime('2022-11-04', '%Y-%m-%d').date()
        )
        self.assertEqual(
            result[1],
            datetime.datetime.strptime('2022-11-07', '%Y-%m-%d').date()
        )

    def test_get_business_days_range_given_date(self):
        result = self.get_business_days_range(
            start_date=datetime.datetime.strptime(
                '2022-11-04', '%Y-%m-%d').date(),
            end_date=datetime.datetime.strptime(
                '2022-11-07', '%Y-%m-%d').date()
        )
        self.assertEqual(
            result[0],
            datetime.datetime.strptime('2022-11-04', '%Y-%m-%d').date()
        )
        self.assertEqual(
            result[1],
            datetime.datetime.strptime('2022-11-07', '%Y-%m-%d').date()
        )

    def test_check_isvalid_range_date_result_true(self):
        result = self.check_isvalid_range_date(
            start_date='2022-11-04',
            end_date='2022-11-07'
        )
        self.assertEqual(result, True)

    def test_check_isvalid_range_date_result_false_smaller(self):
        result = self.check_isvalid_range_date(
            start_date='2022-11-07',
            end_date='2022-11-04'
        )
        self.assertEqual(result, False)

    def test_check_isvalid_range_date_result_false_equal(self):
        result = self.check_isvalid_range_date(
            start_date='2022-11-07',
            end_date='2022-11-07'
        )
        self.assertEqual(result, False)
