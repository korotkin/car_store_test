import pytest

from car_store.store.factories import CarFactory


@pytest.fixture()
@pytest.mark.django_db
def cars():
    for i in range(100):
        CarFactory()
