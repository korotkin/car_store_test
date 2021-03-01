from typing import Any

from django.db.models.expressions import F
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import JsonResponse, HttpResponse
from django.views.generic.base import View
from django.views.generic.list import ListView

from car_store.rates.forms import ExchangeRequestForm
from car_store.rates.utils import NonWorkingTime, ConvertAPI, \
    UnsupportedCurrencyException


class RateConvertlList(View):

    def post(self, request, *args, **kwargs) -> JsonResponse:
        """
        # Part 1.
        Implement REST API for converting currencies - from RUB to other
         available currencies or available currencies to RUB. Your REST API
         may include single endpoint that should receive necessary data from
         client (amount of money, initial currency, target currency) and return
         converted value. Available currencies and exchange rates can be
         requested from CBR API - https://www.cbr-xml-daily.ru/daily_json.js
        """
        form = ExchangeRequestForm(request.POST)
        if form.is_valid():
            amount, initial, target = form.cleaned_data.values()

            try:
                value = ConvertAPI().convert(amount, initial, target)
            except NonWorkingTime:
                return JsonResponse(
                    {"error": "Non working time"}, safe=False, status=400
                )
            except UnsupportedCurrencyException:
                return JsonResponse(
                    {"error": "Unsupurted currency"}, safe=False, status=400
                )

            data = {
                "value": value,
            }
            return JsonResponse(data, status=200)
        else:
            return JsonResponse(form.errors, safe=False, status=400)


rate_convert_list_view = RateConvertlList.as_view()
