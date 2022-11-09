from django.urls import path

from . import views

app_name = 'rates'

urlpatterns = [
    path(
        '',
        views.DateValuesView.as_view(),
        name='form_data'
    ),
    path(
        'api/v1/',
        views.CurrencyRatesApiV1.as_view(),
        name='currency_rates_api_v1'
    ),
]
