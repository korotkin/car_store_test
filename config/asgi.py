"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys

from channels.auth import AuthMiddlewareStack
from channels.routing import ChannelNameRouter, ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# This allows easy placement of apps within the interior
# django_apps directory.
from car_store.rates import consumers as rates_consumers
from car_store.rates import routing as rates_routing

app_path = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
)
sys.path.append(os.path.join(app_path, "django_apps"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        # "websocket": rates_routing.websocket_urlpatterns,
        "websocket": AuthMiddlewareStack(
            URLRouter(rates_routing.websocket_urlpatterns),
        ),
        # "channel": ChannelNameRouter({
        #     "send-changes": rates_consumers.RatesConsumer.as_asgi(),
        # })
    }
)
