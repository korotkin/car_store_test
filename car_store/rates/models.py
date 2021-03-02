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
