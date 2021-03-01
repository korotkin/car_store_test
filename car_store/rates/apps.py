from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StoreConfig(AppConfig):
    name = "car_store.rates"
    verbose_name = _("Currency Rates")
