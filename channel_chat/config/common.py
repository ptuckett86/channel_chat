"""
Django settings for channel_chat project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import datetime
import os
from os.path import join

from configurations import Configuration
from celery.schedules import crontab
from manage import get_secret


class Common(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
    DATABASES = {"default": get_secret("secret_DB")}
    SECRET_KEY = get_secret("SECRET_KEY")
    FERNET_KEY = get_secret("FERNET_KEY")
    EMAIL_HOST = get_secret("EMAIL")
    EMAIL_PORT = 25
    REDIS_HOST = get_secret("REDIS")
    REDIS_PORT = "6379"
    REDIS_URL = "{}:{}".format(REDIS_HOST, REDIS_PORT)
    POSTGRES_HOST = get_secret("POSTGRES")
    POSTGRES_PORT = "5432"
    POSTGRES_URL = "{}:{}".format(POSTGRES_HOST, POSTGRES_PORT)
    DJANGO_HOST = get_secret("DJANGO")
    DJANGO_PORT = "8000"
    LOGIN_URL = "/api/v1/auth/login/"
    ASGI_APPLICATION = "channel_chat.routing.application"
    ROOT_URLCONF = "channel_chat.urls"
    APPEND_SLASH = True
    TIME_ZONE = "UTC"
    LANGUAGE_CODE = "en-us"
    USE_I18N = False
    USE_L10N = True
    USE_TZ = True
    LOGIN_REDIRECT_URL = "/"
    AUTH_USER_MODEL = "core.AuthUser"
    BROKER_URL = "redis://{}".format(REDIS_URL)
    CELERY_RESULT_BACKEND = BROKER_URL
    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_TIMEZONE = "UTC"
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), "static")
    STATIC_URL = "/static/"
    STATICFILES_DIRS = []
    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")
    MEDIA_URL = "/media/"
    ALLOWED_HOSTS = []
    INSTALLED_APPS = [
        "channels",
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_filters",
        "corsheaders",
        "gunicorn",
        "rest_framework",
        "core",
        "chat",
    ]
    MIDDLEWARE = [
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "middleware.AuthenticationMiddlewareJWT",
    ]

    STATICFILES_FINDERS = (
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    )

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": STATICFILES_DIRS,
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]
    AUTHENTICATION_BACKENDS = ("core.backends.ChannelChatBackend",)
    # Django Rest Framework
    REST_FRAMEWORK = {
        "DEFAULT_PAGINATION_CLASS": "core.pagination.CustomPagination",
        "PAGE_SIZE": 10,
        "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
        "DEFAULT_RENDERER_CLASSES": (
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
            "rest_framework_xml.renderers.XMLRenderer",
        ),
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
        "DEFAULT_AUTHENTICATION_CLASSES": (
            "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
            "rest_framework.authentication.BasicAuthentication",
        ),
        "DEFAULT_FILTER_BACKENDS": (
            "django_filters.rest_framework.DjangoFilterBackend",
        ),
    }
    JWT_AUTH = {
        "JWT_ENCODE_HANDLER": "rest_framework_jwt.utils.jwt_encode_handler",
        "JWT_DECODE_HANDLER": "rest_framework_jwt.utils.jwt_decode_handler",
        "JWT_PAYLOAD_HANDLER": "rest_framework_jwt.utils.jwt_payload_handler",
        "JWT_RESPONSE_PAYLOAD_HANDLER": "core.jwt_overrides.jwt_response_payload_handler",
        "JWT_SECRET_KEY": SECRET_KEY,
        "JWT_PUBLIC_KEY": None,
        "JWT_PRIVATE_KEY": None,
        "JWT_ALGORITHM": "HS256",
        "JWT_VERIFY": True,
        "JWT_VERIFY_EXPIRATION": True,
        "JWT_LEEWAY": 0,
        "JWT_EXPIRATION_DELTA": datetime.timedelta(hours=1),
        "JWT_AUDIENCE": None,
        "JWT_ISSUER": None,
        "JWT_ALLOW_REFRESH": True,
        "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(days=7),
        "JWT_AUTH_COOKIE": "jwt",
    }
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [(REDIS_HOST, REDIS_PORT)]},
        }
    }
