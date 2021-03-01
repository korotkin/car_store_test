import csv
import os
import uuid

from django.core.management import BaseCommand
from django.core.management.base import CommandError

from car_store.store.models import (
    Car,
    CarBodyType,
    CarColor,
    CarFuelType,
    CarMake,
    CarModel,
    CarSubmodel,
    CarTransmission,
)


def get_entity_by_name(class_name, value):
    if bool(value):
        obj, created = class_name.objects.get_or_create(name=value)
        return obj.id


class Command(BaseCommand):

    help = "Loads sample data into database. Adapts to the DB schema"

    makes = {}

    def load_makes(self):
        res = []
        filename = os.path.join("data", "makes.csv")
        with open(filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["slug"] = row.pop("id")
                res.append(CarMake(**row))
        CarMake.objects.bulk_create(res)

    def load_models(self):
        res = []
        filename = os.path.join("data", "models.csv")
        with open(filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["slug"] = row.pop("id")
                obj = CarMake.objects.get(slug=row["make_id"])
                row["make_id"] = obj.id
                res.append(CarModel(**row))
        CarModel.objects.bulk_create(res)

    def load_submodels(self):
        res = []
        filename = os.path.join("data", "submodels.csv")
        with open(filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row["slug"] = row.pop("id")
                obj = CarModel.objects.get(slug=row["model_id"])
                row["model_id"] = obj.id
                res.append(CarSubmodel(**row))
        CarSubmodel.objects.bulk_create(res)

    def load_cars(self):
        res = []
        filename = os.path.join("data", "cars.csv")
        with open(filename, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Raise ValueError with wrong UUID
                    uuid.UUID(row["id"])

                    if row["price"] == "":
                        del row["price"]
                    if row["mileage"] == "":
                        del row["mileage"]
                    make = CarMake.objects.get(slug=row["make_id"])
                    row["make_id"] = make.id

                    model = CarModel.objects.filter(make=make).get(slug=row["model_id"])
                    row["model_id"] = model.id

                    submodel = CarSubmodel.objects.get(slug=row["submodel_id"])
                    row["submodel_id"] = submodel.id

                    row["body_type_id"] = get_entity_by_name(
                        CarBodyType, row.pop("body_type")
                    )
                    row["transmission_id"] = get_entity_by_name(
                        CarTransmission, row.pop("transmission")
                    )
                    row["fuel_type_id"] = get_entity_by_name(
                        CarFuelType, row.pop("fuel_type")
                    )
                    row["exterior_color_id"] = get_entity_by_name(
                        CarColor, row.pop("exterior_color")
                    )
                    res.append(Car(**row))
                except Exception as e:
                    self.stdout.write(f"Can't load row {row['id']}")
        Car.objects.bulk_create(res)

    def handle(self, *args, **options):
        if CarMake.objects.exists():
            raise CommandError("Failed: Already loaded")

        # Some checks regarding data integrity were skipped.
        # bulk_create chunks weren't used

        self.load_makes()
        self.load_models()
        self.load_submodels()
        self.load_cars()
        self.stdout.write("Done")
