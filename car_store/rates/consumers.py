import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.http.response import JsonResponse

from car_store.rates.forms import ExchangeRequestForm
from car_store.rates.utils import (
    ConvertAPI,
    NonWorkingTime,
    UnsupportedCurrencyException,
)


class RatesConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "rates"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # TODO: needs to add authentication feature before
        pass
        # try:
        #     data = json.loads(text_data)
        #     form = ExchangeRequestForm(data)
        #     if form.is_valid():
        #         amount, initial, target = form.cleaned_data.values()
        #         value = ConvertAPI().convert(amount, initial, target)
        #     else:
        #         res = {"error": "Non working time"}
        # except NonWorkingTime:
        #     res = {"error": "Non working time"}
        # except UnsupportedCurrencyException:
        #     res = {"error": "Unsupurted currency"}
        # except Exception:
        #     res = {"error": "Server unavailable"}
        # else:
        #     res = {"value": value}
        # user_id = self.context["user"].id
        # async_to_sync(self.channel_layer.group_send)(
        #     f"user-{user_id}", {"type": "rates_message", "message": json.dumps(res)}
        # )

    # Receive message from room group
    def rates_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
