from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/<view_station>/", consumers.DataConsumer.as_asgi()),
]
