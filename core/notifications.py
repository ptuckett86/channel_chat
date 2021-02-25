import json

from django.conf import settings
from django.core.mail import send_mail

from tokens import ExpiringTokenGenerator


def _send_confirmation_email(email):
    token = (
        ExpiringTokenGenerator()
        .generate_token(email)
        .decode("utf-8")
        .replace("=", "%3D")
    )
    # Front end url to take user to confirmation email page
    url = "{}/#/auth/confirm_email/{}".format(settings.DOMAIN, str(token))
    send_mail(
        "Email Confirmation",
        "Click here to confirm your account: {}".format(url),
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )


def send_password_reset_email(email):
    token = (
        ExpiringTokenGenerator()
        .generate_token(email)
        .decode("utf-8")
        .replace("=", "%3D")
    )
    # Front end url to take user to confirmation email page
    url = "{}#/auth/password_reset/{}".format(settings.DOMAIN, str(token))
    send_mail(
        "Password Reset",
        "Click here reset your password: {}".format(url),
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    return token
