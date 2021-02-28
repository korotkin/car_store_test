import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures("cars")
@pytest.mark.django_db
@pytest.mark.parametrize(
    "filter_dict, resp_code, cnt",
    [
        pytest.param(
            {
                "price__gt": 10000,
                "price__lte": 40000,
                "mileage__gt": 10000,
                "mileage__lte": 450000,
            },
            200,
            60,
            id="price-range-mileage-range",
        ),
        pytest.param(
            {
                # "price__gt": None,
                "price__lte": 40000,
                "mileage__gt": 10000,
                "mileage__lte": 450000,
            },
            200,
            70,
            id="price-mex-mileage-range",
        ),
        pytest.param(
            {
                "price__gt": 10000,
                # "price__lte": None,
                "mileage__gt": 10000,
                "mileage__lte": 450000,
            },
            200,
            78,
            id="price-min-mileage-range",
        ),
        pytest.param(
            {
                "price__gt": 10000,
                "price__lte": 40000,
                # "mileage__gt": None,
                "mileage__lte": 450000,
            },
            200,
            60,
            id="price-range-mileage-max",
        ),
        pytest.param(
            {
                "price__gt": 10000,
                "price__lte": 40000,
                "mileage__gt": 10000,
                # "mileage__lte": None,
            },
            200,
            58,
            id="price-range-mileage-min",
        ),
        pytest.param(
            {
                "price__gt": "A",
            },
            400,
            None,
            id="wrong-value-non-integer",
        ),
        pytest.param(
            {
                "price__gt": -1,
            },
            400,
            None,
            id="wrong-value-negative",
        ),
        pytest.param(
            {
                "model__name__icontains": "model",
                "submodel__name__icontains": "submodel",
            },
            200,
            100,  # TODO: needs to solve issue with PK in fabric
            id="text-filter",
        ),
    ],
)
def test_car_list_filter_success(client, filter_dict, resp_code, cnt):
    url = reverse("v1-store:car-list")
    res = client.get(url, data=filter_dict)
    assert res.status_code == resp_code
    if resp_code == 200:
        data = res.json()
        assert len(data) == cnt
