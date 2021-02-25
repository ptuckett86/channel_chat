from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from core.models import AuthUser
from chat.models import ChatHistory, Room


@database_sync_to_async
def add_room(room_name, participants, pk, part_type):
    if pk:
        room, created = Room.objects.get_or_create(pk=pk, participantType=part_type)
        if created:
            room.participants = participants
            room.name = room_name
            room.save()
    else:
        room, created = Room.objects.get_or_create(
            participants=participants, name=room_name, participantType=part_type
        )
    return str(room.pk), created


@database_sync_to_async
def save_messages(from_user, participants, room_id, content, part_type):
    # get or create the room associated to the sorted participants and then name
    room = Room.objects.get(pk=room_id)
    # iterate over each person
    for person in participants:
        # get the users to create a new chat history item
        to_user = AuthUser.objects.get(pk=person)
        # create new history item
        history = ChatHistory.objects.create(
            message=content["message"]["message"],
            owner=from_user,
            to=to_user,
            room=room,
            read=False,
        )
        return str(history.pk)


@database_sync_to_async
def read_history(history_id):
    history = ChatHistory.objects.get(pk=history_id)
    if history:
        history.read = True
        history.save()
    return history


class SocketConsumer(AsyncJsonWebsocketConsumer):
    """
    Websocket class that handles web socket connection and traffic.
    """

    async def connect(self):
        """
        Verifies the users access and connects to the websocket.
        """
        try:
            # gets user from scope
            user = self.scope["user"]
            # if user is anonymous close connection
            if user.is_anonymous:
                await self.close()
            else:
                # open websocket
                self.groups = []
                if str(user.pk) not in self.groups:
                    await self.channel_layer.group_add(str(user.pk), self.channel_name)
                    self.groups.append(str(user.pk))
                await self.accept()
        except:
            await self.close()

    async def receive_json(self, content):
        """
        Called when we get a text frame. Channels will JSON-decode the payload
        for us and pass it as the first argument.
        """
        if content["message_type"] == "chat":
            # get the original participants
            og_parts = content["participants"]
            # initialize the list
            new_parts = []
            # add the fromid to the new list
            new_parts.append(content["message"]["fromId"])
            # iterate over original participants
            for user_id in og_parts:
                # add the old participants to the new participants list
                new_parts.append(user_id)
            # sort the list
            sorted_parts = sorted(new_parts)
            user = self.scope["user"]
            part_type = content["participantType"]
            if part_type == 1:
                group_id = content["message"]["toId"]
                name = content["displayName"]
                room_id, created = await add_room(
                    name, sorted_parts, group_id, part_type
                )
                if group_id not in self.groups:
                    await self.channel_layer.group_add(group_id, self.channel_name)
                    if created:
                        for participant in sorted_parts:
                            await self.channel_layer.group_send(
                                participant,
                                {
                                    "type": "add.message",
                                    "participantType": part_type,
                                    "participants": sorted_parts,
                                    "group_id": group_id,
                                    "displayName": name,
                                },
                            )
                    self.groups.append(group_id)
            else:
                name = "{}-two-way".format("-".join(sorted_parts))
                group_id = None
                room_id, created = await add_room(name, sorted_parts, None, part_type)
                if str(user.pk) not in self.groups:
                    await self.channel_layer.group_add(str(user.pk), self.channel_name)
                    self.groups.append(str(user.pk))

            # check if the list is greater than 1
            history_id = await save_messages(
                user, sorted_parts, room_id, content, part_type
            )
            if part_type == 1:
                for participant in sorted_parts:
                    await self.channel_layer.group_send(
                        participant,
                        {
                            "type": "chat.message",
                            "participants": content["participants"],
                            "message": content["message"],
                            "participantType": part_type,
                            "history_id": history_id,
                        },
                    )
            else:
                for user in og_parts:
                    await self.channel_layer.group_send(
                        user,
                        {
                            "type": "chat.message",
                            "participants": content["participants"],
                            "message": content["message"],
                            "participantType": part_type,
                            "history_id": history_id,
                        },
                    )
        else:
            # send note messages to current uusers
            user = str(user.pk)
            await self.channel_layer.group_send(
                user,
                {"type": "note.message", "room": user, "message": content["message"]},
            )

    async def disconnect(self, code):
        """
        Called when the WebSocket closes for any reason.
        """
        # Leave all the rooms we are still in
        for group in self.groups:
            await self.channel_layer.group_discard(group, self.channel_name)

    async def note_message(self, event):
        """
        Transmit notification message to room
        """
        message = {
            "message_type": "notification",
            "room": event["room"],
            "message": event["message"],
        }
        await self.send_json(message)

    async def chat_message(self, event):
        """
        Transmit chat message to room
        """

        await read_history(event["history_id"])
        event["message_type"] = "chat"
        del event["type"]
        del event["history_id"]
        await self.send_json(event)

    async def add_message(self, event):
        await self.send_json(event)
