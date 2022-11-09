
import json

import requests  # type: ignore

from ..models import CurrencyRate  # type: ignore


class Currency:
    def get_currency_from_api(self, date, url='https://api.vatcomply.com'):
        """
        date: datetime
        return: returns the currency rate values from date
        """

        str_date = date.strftime("%Y-%m-%d")
        endpoint_request = '/rates?base=USD&date='+str_date

        try:
            response = requests.get(
                url+endpoint_request
            )
        except requests.exceptions.ConnectionError:
            return None

        if response.status_code != 200:
            return None

        response_dict = json.loads(response.text)['rates']

        return {
            'BRL': response_dict.get('BRL', None),
            'EUR': response_dict.get('EUR', None),
            'JPY': response_dict.get('JPY', None),
        }

    def get_range_currencies(self, range_date):
        """
        range_date: a list of days (timestamps)

        try to find date on database if not exist it requests to api

        return: returns a list of dictonaries with data and respective rates
        """

        data_list = []
        for date in range_date:

            currencyRate = CurrencyRate.objects.filter(date=date).first()

            if currencyRate is not None:
                rates = {
                    'BRL': currencyRate.brl_rate,
                    'EUR': currencyRate.eur_rate,
                    'JPY': currencyRate.jpy_rate,
                }
            else:
                rates = self.get_currency_from_api(date)
                CurrencyRate.objects.create(
                    date=date,
                    brl_rate=rates.get('BRL', None),
                    eur_rate=rates.get('EUR', None),
                    jpy_rate=rates.get('JPY', None)
                )

            data_list.append(
                {
                    'date': date.strftime("%Y-%m-%d"),
                    'rates': rates
                }
            )

        return data_list
