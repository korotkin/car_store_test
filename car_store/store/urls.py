from django.urls import path

from car_store.store.views import (
    submodule_list_view,
    car_list_view,
)

app_name = "users"
urlpatterns = [
    path("submodule/", view=submodule_list_view, name="submodule-list"),
    path("car/", view=car_list_view, name="car-list"),
]
