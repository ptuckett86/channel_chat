"""
WSGI config for channel_chat project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

env = get_secret("ENVIRONMENT").capitalize()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "channel_chat.config")
os.environ.setdefault("DJANGO_CONFIGURATION", env)

application = get_wsgi_application()
