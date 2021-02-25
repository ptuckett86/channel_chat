from channels.db import database_sync_to_async
from channels.auth import AuthMiddlewareStack

from django.contrib.auth.models import AnonymousUser

from http import cookies

from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler

from core.models import AuthUser


def get_jwt_value(scope):
    try:
        cookie = next(x for x in scope["headers"] if x[0].decode("utf-8") == "cookie")[
            1
        ].decode("utf-8")
        return cookies.SimpleCookie(cookie)["jwt"].value
    except:
        cookie = scope["query_string"]
        return cookie


@database_sync_to_async
def get_user(user_id):
    try:
        return AuthUser.objects.get(pk=user_id)
    except AuthUser.DoesNotExist:
        return AnonymousUser()


class JsonTokenAuthMiddleware(BaseJSONWebTokenAuthentication):
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):

        try:
            jwt_value = get_jwt_value(scope)
            user_id = jwt_decode_handler(jwt_value).get("user_id")
            user = await get_user(user_id)
            scope["user"] = user
        except:
            scope["user"] = AnonymousUser()
        return await self.app(scope, receive, send)
