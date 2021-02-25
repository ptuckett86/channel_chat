from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import JSONWebTokenAPIView


from core.serializers import *
from core.notifications import _send_confirmation_email, send_password_reset_email
from core.permissions import IsSuperUser
from core.filters import *
from core.pagination import FlexiblePagination
from tokens import ExpiringTokenGenerator


class UserViewSet(viewsets.ModelViewSet):
    """
    All users regardless of type. Only Super Users can see this.
    """

    pagination_class = FlexiblePagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_class = UserFilter
    search_fields = ["uuid", "first_name", "last_name", "middle_name", "email"]

    def get_queryset(self):
        user = self.request.user
        if self.request.is_superuser:
            return AuthUser.objects.all()
        else:
            return AuthUser.objects.filter(pk=user.pk)

    def get_serializer_class(self):
        return UserReadSerializer

    def get_permissions(self):
        if self.request.is_superuser:
            return [IsSuperUser()]
        else:
            return [IsAuthenticated()]


class LoginHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = LoginHistoryReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return LoginHistory.objects.all()
        else:
            return LoginHistory.objects.filter(user=user)


class LoginObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.

    Returns a JSON Web Token that can be used for authenticated requests.
    """

    serializer_class = LoginJSONWebTokenSerializer

    def post(self, request):

        response = super().post(request)
        if response.data.get("security_code"):
            response.delete_cookie("jwt")
        return response


login_obtain_jwt_token = LoginObtainJSONWebToken.as_view()


class ResendEmailConfirmToken(APIView):
    """Sends an email confirmation link."""

    serializer_class = ResendEmailSerializer

    def post(self, request, format=None):
        serializer = ResendEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            _send_confirmation_email(email)
            return Response(
                "Confirmation email sent to: {}.".format(email),
                status=status.HTTP_200_OK,
            )


class EmailConfirmView(APIView):
    """Confirms an email from the passed in url token."""

    def get(self, request, token):
        email = ExpiringTokenGenerator().get_token_value(token)
        try:
            user = AuthUser.objects.get(email=email)
        except:
            user = None
        if user:
            user.email_confirmed = True
            return Response("Email Confirmed", status=status.HTTP_200_OK)
        else:
            return Response("Email token expired")


class ObtainEmailPasswordResetToken(APIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, format=None):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            token = send_password_reset_email(user)
            return Response(token, status=status.HTTP_200_OK)


class PasswordResetView(APIView):
    serializer_class = ChangePasswordSerializer

    def post(self, request, token):
        email = ExpiringTokenGenerator().get_token_value(token)
        try:
            user = AuthUser.objects.get(email=email)
        except:
            user = None
        if user:
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user.set_password(serializer.validated_data["password"])
                user.save()
                return Response("Password Changed", status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                "Reset password email no longer valid",
                status=status.HTTP_400_BAD_REQUEST,
            )
