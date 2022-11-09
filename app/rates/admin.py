from django.contrib import admin
from .models import CurrencyRate

class CurrencyRateAdmin(admin.ModelAdmin):
    pass

admin.site.register(CurrencyRate, CurrencyRateAdmin)