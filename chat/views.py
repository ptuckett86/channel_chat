from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter

from core.pagination import FlexiblePagination
from chat.filters import ChatHistoryFilter, RoomFilter
from chat.models import ChatHistory, Room
from chat.serializers import ChatHistorySerializer, RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    pagination_class = FlexiblePagination
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_class = RoomFilter
    search_fields = ["uuid", "name", "participants"]

    def get_queryset(self):
        return Room.objects.all()

    def get_serializer_class(self):
        return RoomSerializer


class ChatHistoryViewSet(viewsets.ModelViewSet):
    pagination_class = FlexiblePagination
    permission_classes = [IsAuthenticated]
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_class = ChatHistoryFilter
    ordering_fields = ("owner__email", "room__name", "to__email")
    search_fields = (
        "uuid",
        "owner__email",
        "room__participants",
        "room__name",
        "message",
        "to__email",
    )

    def get_queryset(self):
        return ChatHistory.objects.all()

    def get_serializer_class(self):
        self.http_method_names = ["get"]
        return ChatHistorySerializer
