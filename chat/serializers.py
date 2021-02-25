from django.db import transaction

from rest_flex_fields import FlexFieldsModelSerializer
from rest_framework import serializers

from chat.models import ChatHistory, Room


class RoomSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Room
        fields = ["url", "uuid", "name", "participants"]


class ChatHistorySerializer(FlexFieldsModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ["url", "uuid", "created_at", "owner", "room", "message", "to", "read"]
        read_only_fields = ["url", "uuid", "owner", "read"]
