from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from uuid import uuid4

from core.managers import UserManager


class MetaModel(models.Model):
    """
    Provides information common to most every object in the database.
    """

    uuid = models.UUIDField(
        default=uuid4, editable=False, db_index=True, unique=True, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class AuthUser(MetaModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField()
    jwt_secret = models.UUIDField(default=uuid4)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["email"]

    @property
    def full_name(self):
        if self.middle_name:
            return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)
        else:
            return "{} {}".format(self.first_name, self.last_name)


class LoginHistory(MetaModel):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    host = models.CharField(max_length=250)
    platform = models.CharField(max_length=350)
    attempt = models.BooleanField(default=False)

    @property
    def last_login(self):
        return user.last_login
