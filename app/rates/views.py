import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import CurrencyRate
from .tools.date_tools import DateTools
from .tools.request_currency import Currency


class DateValuesView(View, Currency, DateTools):
    http_method_names = ['get', 'post']

    def _render_empty_data(self, request):
        return render(
            request, 'rates/pages/graphics.html',
            context={
                'data': False
            }
        )

    def get(self, request, data=None):
        return self._render_empty_data(request)

    def post(self, request):

        start_date = request.POST.get('start')
        end_date = request.POST.get('end')
        currency = request.POST.get('currency')
        business_days = self.get_business_days_range(start_date, end_date)

        if not self.check_end_date_is_up_today(end_date):
            messages.error(
                request,
                'End date must be earlier or equal than today'
            )
            return self._render_empty_data(request)

        if len(business_days) == 1 or not \
                self.check_isvalid_range_date(start_date, end_date):
            messages.error(
                request,
                'Start date must be earlier than End date'
            )
            return self._render_empty_data(request)

        if len(business_days) > 5:
            messages.error(request, 'Maximum of 5 business days')
            return self._render_empty_data(request)

        data_response = self.get_range_currencies(
            range_date=business_days
        )

        values_currency = []
        dates = []
        for response in data_response:
            values_currency.append(
                response.get('rates').get(currency)
            )
            dates.append(
                response.get('date')
            )

        data = [{
            'name': currency,
            'data': values_currency
        }]

        return render(
            request, 'rates/pages/graphics.html',
            context={
                'data': json.dumps(data),
                'dates': json.dumps(dates),
                'currency': currency
            }
        )


class CurrencyRatesApiV1(View):
    http_method_names = ['get']

    def get(self, request):
        all_currencies = CurrencyRate.objects.all().values(
            'date', 'brl_rate', 'eur_rate', 'jpy_rate'
        )

        return JsonResponse(
            list(all_currencies),
            safe=False
        )
