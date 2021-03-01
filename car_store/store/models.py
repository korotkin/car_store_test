import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.base import Model


class CarMake(Model):
    slug = models.SlugField(db_index=True, max_length=50, editable=False)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CarModel(Model):
    slug = models.SlugField(db_index=True, max_length=50, editable=False)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CarSubmodel(Model):
    slug = models.SlugField(db_index=True, max_length=50, editable=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=False)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AbstractEntityModel(Model):
    name = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class CarTransmission(AbstractEntityModel):
    pass


class CarColor(AbstractEntityModel):
    pass


class CarBodyType(AbstractEntityModel):
    pass


class CarFuelType(AbstractEntityModel):
    pass


class Car(Model):
    id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4)
    active = models.BooleanField(default=False)
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2050),
        ]
    )
    mileage = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)

    make = models.ForeignKey(CarMake, on_delete=models.PROTECT)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    submodel = models.ForeignKey(CarSubmodel, on_delete=models.PROTECT)

    body_type = models.ForeignKey(
        CarBodyType, null=True, blank=True, on_delete=models.SET_NULL
    )
    transmission = models.ForeignKey(
        CarTransmission, null=True, blank=True, on_delete=models.SET_NULL
    )
    fuel_type = models.ForeignKey(
        CarFuelType, null=True, blank=True, on_delete=models.SET_NULL
    )
    exterior_color = models.ForeignKey(
        CarColor, null=True, blank=True, on_delete=models.SET_NULL
    )

    # TODO:  auto_now_add=True must be returned after loading data
    created_at = models.DateTimeField()
    # TODO:  auto_now=True must be returned after loading data
    updated_at = models.DateTimeField()
