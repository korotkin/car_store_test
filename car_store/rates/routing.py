from django.urls import re_path

from car_store.rates import consumers

websocket_urlpatterns = [
    re_path(r"ws/rates/$", consumers.RatesConsumer.as_asgi()),
]
