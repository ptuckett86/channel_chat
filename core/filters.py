import django_filters

from core.models import AuthUser


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = AuthUser
        fields = {
            "uuid": ["exact"],
            "first_name": ["icontains"],
            "last_name": ["icontains"],
            "middle_name": ["icontains"],
            "email": ["icontains"],
        }
