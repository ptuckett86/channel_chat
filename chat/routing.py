from django.urls import path

from chat import consumers

websocket_urlpatterns = [path("ws/<str:uuid>/", consumers.SocketConsumer.as_asgi())]
