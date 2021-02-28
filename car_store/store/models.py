import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.base import Model


class CarMake(Model):
    id = models.SlugField(primary_key=True, max_length=50, editable=False)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CarModel(Model):
    id = models.SlugField(primary_key=True, max_length=50, editable=False)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CarSubmodel(Model):
    id = models.SlugField(primary_key=True, max_length=50, editable=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=False)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Car(Model):
    id = models.UUIDField(
        primary_key=True, db_index=True, default=uuid.uuid4, editable=False
    )
    active = models.BooleanField(default=False)
    year = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(2050),
        ]
    )
    mileage = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    make = models.ForeignKey(CarMake, on_delete=models.PROTECT)
    model = models.ForeignKey(CarModel, on_delete=models.PROTECT)
    submodel = models.ForeignKey(CarSubmodel, on_delete=models.PROTECT)

    body_type = models.PositiveIntegerField(null=True, blank=True)
    transmission = models.PositiveIntegerField(null=True, blank=True)
    fuel_type = models.PositiveIntegerField(null=True, blank=True)
    exterior_color = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
