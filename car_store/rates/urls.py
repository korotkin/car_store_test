from django.urls import path

from car_store.rates.views import rate_convert_list_view

app_name = "users"
urlpatterns = [
    path("convert/", view=rate_convert_list_view, name="rate_convert-list"),
]
