from typing import Any

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.views.generic.list import ListView

from car_store.store.forms import CarModelForm, CarSearchForm
from car_store.store.models import Car, CarMake, CarModel, CarSubmodel


class SubmodelList(ListView):
    def get_queryset(self) -> QuerySet:
        return CarSubmodel.objects.select_related("model", "model__make")

    def get(self, request) -> JsonResponse:
        """
        List all makes, models, and submodels
        """
        makes_qs = CarMake.objects.filter(active=True).values("id", "name")
        models_qs = CarModel.objects.filter(active=True).values("id", "name", "make_id")
        submodels_qs = CarSubmodel.objects.filter(active=True).values(
            "id", "name", "model_id"
        )
        res = {
            "makes": list(makes_qs),
            "models": list(models_qs),
            "submodels": list(submodels_qs),
        }
        return JsonResponse(res, safe=False)


submodule_list_view = SubmodelList.as_view()


class CarList(ListView):
    def get_queryset(self) -> QuerySet:
        return Car.objects.select_related("submodel", "model", "make").order_by(
            "-updated_at"
        )

    def get(self, request: HttpRequest):
        """
        Task:
        1. List all cars with their matching make, model and submodel names
        2. Query cars within a certain price and mileage and return a list of
        matches sorted by updated_at (where the newest element is first)
        Include the car names here as well

        GET query params:
         - page: int|None - page number
         - price__gt: int, car price
         - price__lte: int
         - mileage__gt: int, car mileage
         - mileage__lte: int
        """
        keys = ("id", "make", "model", "submodel")
        # Prepare query with joining data at the server side
        queryset = self.get_queryset().values_list(
            "id",
            "make__name",
            "model__name",
            "submodel__name",
        )

        # Search. Used the most easyest way. From my perspective mo efficient is
        # using DRF ListAPIView and django_filters module
        # Same with filter attributes name. There is no strong assumptions.
        form = CarSearchForm(request.GET)
        if form.is_valid():
            # Remove empty values from the filter
            filter_dict = {}
            for k, v in form.cleaned_data.items():
                if v:
                    filter_dict[k] = v
            queryset = queryset.filter(**filter_dict)
        else:
            return JsonResponse(form.errors, safe=False, status=400)

        # Add pagination if it's requested
        page_size = self.get_paginate_by(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, page_size
            )

        # Convert list of lists to the list of dict
        res = [dict(zip(keys, row)) for row in queryset]
        return JsonResponse(res, safe=False)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """
        Task:
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = CarModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(status=200)
        else:
            return JsonResponse(form.errors, safe=False, status=400)


car_list_view = CarList.as_view()
