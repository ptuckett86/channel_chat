#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import json

from django.core.exceptions import ImproperlyConfigured

with open("secrets.json") as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


def main():
    """Run administrative tasks."""
    env = get_secret("ENVIRONMENT").capitalize()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channel_chat.config")
    os.environ.setdefault("DJANGO_CONFIGURATION", env)
    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
