"""
ASGI config for channel_chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

env = get_secret("ENVIRONMENT").capitalize()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channel_chat.config")
os.environ.setdefault("DJANGO_CONFIGURATION", env)

application = get_asgi_application()
