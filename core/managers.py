from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(extra_fields.get("email"))
        is_superuser = extra_fields.pop("is_superuser")
        user, created = self.model.objects.get_or_create(
            is_superuser=is_superuser, **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_user(self, password=None, *args, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("email_confirmed", False)
        return self._create_user(password, **extra_fields)

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("email_confirmed", True)
        return self._create_user(password, **extra_fields)
