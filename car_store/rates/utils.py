from datetime import time

import requests
from django.core.cache import cache
import arrow

RATES_DAILY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


class NonWorkingTime(Exception):
    pass


class UnsupportedCurrencyException(Exception):
    pass


class ConvertAPI:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    client = None
    data = None

    def __init__(self):
        """
        get cached request. refresh if outdated
        calculate and return value
        """
        self.client = requests.Session()
        self.client.headers.update(self.headers)

        self.data = cache.get("currency")
        if self.data is None or not self.check_date(self.data):
            self.data = self.update_currency()

    def check_date(self, data):
        """
        Note 2. Let's imagine that exchange rates are updated in CBR API from 9:00
        AM till midnight and can be updated every 5 min (for example, at 9:00 AM, 9:05 AM, 9:10 AM etc., but also can stay the same during some time - 15 min, for example).

        :param data:
        :return:
        """
        if time(9, 0, 0) > arrow.now().time() > time(23, 59, 59):
            raise NonWorkingTime()

        date_diff = arrow.now() - arrow.get(data["Timestamp"])
        return date_diff.total_seconds() < 900

    def update_currency(self):
        res = self.client.get(RATES_DAILY_URL)
        data = res.json()
        cache.set("currency", data, 900)
        return data

    def convert(self, amount, initial, target) -> float:
        """
        :param amount:
        :param initial:
        :param target:
        :return:
        """

        try:
            initial_rate = self.data["Valute"][initial]["Value"]
            target_rate = self.data["Valute"][target]["Value"]
        except KeyError:
            raise UnsupportedCurrencyException()
        return amount / initial_rate * target_rate
