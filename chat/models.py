from django.db import models

from core.models import MetaModel


class Room(MetaModel):
    name = models.CharField(max_length=255, null=True)
    participantType = models.IntegerField(default=0)
    participants = models.JSONField(null=True)


class ChatHistory(MetaModel):
    owner = models.ForeignKey("core.AuthUser", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    to = models.ForeignKey(
        "core.AuthUser", on_delete=models.CASCADE, null=True, related_name="recipient"
    )
    read = models.BooleanField(default=False)
