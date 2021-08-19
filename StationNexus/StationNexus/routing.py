from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path("ws/kiosk/<view_station>/", consumers.DataConsumer.as_asgi()),
    path("ws/test/<view_station>/", consumers.TestConsumer.as_asgi()),
]
