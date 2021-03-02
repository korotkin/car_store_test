import pytest
from django.test import TestCase
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestView(TestCase):
    def test_rates_convert_success(self):
        url = reverse("v1-store:rate_convert-list")
        data = {
            "amount": 1,
            "initial": "USD",
            "target": "EUR",
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertListEqual(
            list(data.keys()),
            [
                "value",
            ],
        )

    def test_rates_convert_form_fail(self):
        url = reverse("v1-store:rate_convert-list")
        data = {
            "amount": 1,
            "initial": "XXXX",
            "target": "EUR",
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 400)
        data = res.json()

    def test_rates_convert_unknown_currency_fail(self):
        url = reverse("v1-store:rate_convert-list")
        data = {
            "amount": 1,
            "initial": "XXX",
            "target": "EUR",
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 400)
        data = res.json()

    # Request in unworking time

    # Request in unworking time
