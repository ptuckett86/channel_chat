from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from chat.routing import websocket_urlpatterns
from chat.middleware import JsonTokenAuthMiddleware


application = ProtocolTypeRouter(
    {
        # (http->django views is added by default)
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            JsonTokenAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
