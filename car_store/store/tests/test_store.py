import pytest
from django.test import TestCase
from django.urls import reverse
from django.utils.http import urlencode

from car_store.store.factories import (
    CarFactory,
    CarMakeFactory,
    CarModelFactory,
    CarSubmodelFactory,
)
from car_store.store.models import Car, CarMake, CarModel, CarSubmodel

pytestmark = pytest.mark.django_db


class TestView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(100):
            make = CarMakeFactory()
            model = CarModelFactory(make=make)
            submodel = CarSubmodelFactory(model=model)
            CarFactory(make=make, model=model, submodel=submodel)

    def test_submodule_get_list_success(self):
        """
        List all makes, models, and submodels
        """
        url = reverse("v1-store:submodule-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertListEqual(list(data.keys()), ["makes", "models", "submodels"])
        self.assertEqual(len(data["makes"]), CarMake.objects.count())
        self.assertEqual(len(data["models"]), CarModel.objects.count())
        self.assertEqual(len(data["submodels"]), CarSubmodel.objects.count())

    def test_car_list_success(self):
        url = reverse("v1-store:car-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data), Car.objects.count())
        self.assertListEqual(list(data[0].keys()), ["id", "make", "model", "submodel"])

    def test_car_create_success(self):
        url = reverse("v1-store:car-list")
        data = {
            "year": 2000,
            "mileage": 12345,
            "price": 12345,
            "make": "make 0",
            "model": "model 0",
            "submodel": "submodel 0",
            "body_type": "",
            "transmission": "",
            "fuel_type": "",
            "exterior_color": "",
        }
        res = self.client.post(
            url, urlencode(data), content_type="application/x-www-form-urlencoded"
        )
        self.assertEqual(res.status_code, 200)

    def test_car_create_fail(self):
        url = reverse("v1-store:car-list")
        data = {
            "year": 1800,
            "mileage": -1,
            "price": "",
            "make": "X",
            "model": "X",
            "submodel": "X",
            "body_type": "",
            "transmission": "",
            "fuel_type": "",
            "exterior_color": "",
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 400)

        # It is a very basic check. This part can be moved
        # Will be beter to extract this part into a separate test
        self.assertEqual(
            res.json(),
            {
                "mileage": ["Ensure this value is greater than or equal to 0."],
                "make": [
                    "Select a valid choice. That choice is not one of the available choices."
                ],
                "model": [
                    "Select a valid choice. That choice is not one of the available choices."
                ],
                "submodel": [
                    "Select a valid choice. That choice is not one of the available choices."
                ],
                "year": ["Ensure this value is greater than or equal to 1900."],
            },
        )
