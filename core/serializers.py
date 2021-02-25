from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from rest_flex_fields import FlexFieldsModelSerializer

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

from core.models import AuthUser, LoginHistory

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class LoginJSONWebTokenSerializer(JSONWebTokenSerializer):
    """
    Serializer class used to validate a username and password.

    'username' is identified by the custom UserModel.USERNAME_FIELD.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """

    def validate(self, attrs):
        request = self.context["request"]
        email = attrs.get("email")
        password = attrs.get("password")
        credentials = {"email": email, "password": password}
        raw_host = request.stream.META.get("HTTP_X_FORWARDED_FOR", None)
        platform = request.stream.META.get("HTTP_USER_AGENT", None)
        if raw_host:
            host = raw_host.split(",")[0]
        else:
            host = "localhost"
        host_string = host + "_" + platform
        if all(credentials.values()):
            user = authenticate(**credentials, host=host, platform=platform)
            payload = jwt_payload_handler(user)
            return {"token": jwt_encode_handler(payload), "user": user}
        else:
            raise serializers.ValidationError("Credentials could not be verified")


class UserReadSerializer(FlexFieldsModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail")

    class Meta:
        model = AuthUser
        fields = [
            "url",
            "uuid",
            "created_at",
            "updated_at",
            "last_login",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
            "is_superuser",
        ]


class UserCreateSerializer(UserReadSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, min_length=8, max_length=140
    )

    UserReadSerializer.Meta

    def create(self, validated_data):
        user = AuthUser.objects.create_user(**validated_data)
        return user


class LoginHistoryReadSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = LoginHistory
        fields = ["url", "uuid", "host", "platform", "attempt", "user"]

    expandable_fields = {"user": (UserReadSerializer, {"source": "user"})}


class ResendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, help_text="The account to be verified."
    )


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={"input_type": "password"}, required=True)
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate(self, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")
        if not password:
            raise serializers.ValidationError(
                {"password": ["Please enter a new password."]}
            )
        if not confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": ["Please re-enter your new password."]}
            )
        if password != confirm_password:
            raise serializers.ValidationError(
                {
                    "password": ["These passwords don't match."],
                    "confirm_password": ["These passwords don't match."],
                }
            )
        return values


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, help_text="The email associated to the account."
    )
