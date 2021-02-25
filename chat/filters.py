import django_filters

from chat.models import ChatHistory, Room


class ChatHistoryFilter(django_filters.FilterSet):

    room__participants = django_filters.CharFilter(method="filter_participants")

    def filter_participants(self, queryset, name, value):
        return queryset.filter(room__participants__contains=value)

    class Meta:
        model = ChatHistory
        fields = {
            "uuid": ["exact"],
            "owner__email": ["exact"],
            "owner": ["exact"],
            "to": ["exact"],
            "room": ["exact"],
            "room__name": ["exact"],
            "message": ["icontains"],
            "to__email": ["exact"],
            "read": ["exact"],
        }


class RoomFilter(django_filters.FilterSet):

    participants = django_filters.CharFilter(method="filter_participants")

    def filter_participants(self, queryset, name, value):
        return queryset.filter(participants__contains=value)

    class Meta:
        model = Room
        fields = {"uuid": ["exact"], "name": ["exact"]}
