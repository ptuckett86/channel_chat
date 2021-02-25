from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.contrib.auth.backends import ModelBackend
from django.utils import timezone
from rest_framework import exceptions


from core.models import AuthUser, LoginHistory


UserModel = get_user_model()


class ChannelChatBackend(ModelBackend):
    def log_login(self, **kwargs):
        LoginHistory.objects.create(**kwargs)

    def authenticate(self, request, email=None, password=None, **kwargs):
        host = kwargs.get("host", None)
        platform = kwargs.get("platform", None)
        if not email:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        else:
            try:
                user = AuthUser.objects.get(email=email)
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                UserModel().set_password(password)
            else:

                if user:
                    self.log_login(user=user, host=host, platform=platform)
                    if user.check_password(password):
                        active, confirmed = self.user_can_authenticate(user)
                        if active and confirmed:
                            user.last_login = timezone.now()
                            user.save()
                            cache.clear()
                            return user
                        else:
                            raise exceptions.AuthenticationFailed(
                                "Credentials could not be verified"
                            )
                    else:
                        raise exceptions.AuthenticationFailed(
                            "Credentials could not be verified"
                        )
                else:
                    raise exceptions.AuthenticationFailed(
                        "Credentials could not be verified"
                    )

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False or email_confirmed=False.
        """
        is_active = getattr(user, "is_active", None)
        email_confirmed = getattr(user, "email_confirmed", None)
        return is_active, email_confirmed
