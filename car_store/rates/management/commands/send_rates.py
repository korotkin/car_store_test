from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.management.base import BaseCommand

from car_store.rates.utils import ConvertAPI


class Command(BaseCommand):
    channel_layer = get_channel_layer()
    help = "Periodic task to be run every 5 minutes"

    def handle(self, *args, **options):
        rates = ConvertAPI().get_data()
        async_to_sync(self.channel_layer.group_send)(
            "rates", {"type": "rates_message", "message": rates}
        )
