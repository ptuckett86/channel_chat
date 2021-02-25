

from rest_framework.routers import DefaultRouter


from core.views import *
from chat.views import *


router = DefaultRouter()

"""USERS"""
router.register("users", UserViewSet, basename="user")
router.register("login_histories", LoginHistoryViewSet, basename="loginhistory")
"""WEB SOCKET"""
router.register("chathistory", ChatHistoryViewSet, basename="chathistory")
router.register("room", RoomViewSet, basename="room")
