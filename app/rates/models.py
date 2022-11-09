from django.db import models


class CurrencyRate(models.Model):
    date = models.DateField()
    brl_rate = models.FloatField()
    eur_rate = models.FloatField()
    jpy_rate = models.FloatField()
