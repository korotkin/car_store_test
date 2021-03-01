from datetime import datetime

import factory
from factory.django import DjangoModelFactory

from car_store.store.models import Car, CarMake, CarModel, CarSubmodel


class CarMakeFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "make {}".format(n))
    active = True
    created_at = factory.LazyAttribute(lambda x: datetime.now())
    updated_at = factory.LazyAttribute(lambda x: datetime.now())

    class Meta:
        model = CarMake


class CarModelFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "model {}".format(n))
    active = True
    make = factory.SubFactory(CarMakeFactory)
    created_at = factory.LazyAttribute(lambda x: datetime.now())
    updated_at = factory.LazyAttribute(lambda x: datetime.now())

    class Meta:
        model = CarModel


class CarSubmodelFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "submodel {}".format(n))
    active = True
    model = factory.SubFactory(CarModelFactory)
    created_at = factory.LazyAttribute(lambda x: datetime.now())
    updated_at = factory.LazyAttribute(lambda x: datetime.now())

    class Meta:
        model = CarSubmodel


class CarFactory(DjangoModelFactory):

    active = True
    year = 2000
    price = factory.Iterator(range(1000, 50000, 1000))
    mileage = factory.Iterator(range(0, 500000, 10000))

    make = factory.SubFactory(CarMakeFactory)
    model = factory.SubFactory(CarModelFactory)
    submodel = factory.SubFactory(CarSubmodelFactory)

    body_type = None
    transmission = None
    fuel_type = None
    exterior_color = None

    created_at = factory.LazyAttribute(lambda x: datetime.now())
    updated_at = factory.LazyAttribute(lambda x: datetime.now())

    class Meta:
        model = Car
