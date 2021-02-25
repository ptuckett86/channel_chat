from .common import Common


class Prod(Common):
    DEBUG = False
    DOMAIN = "example.com"
    PROTOCOL = "https"
    CORS_ALLOW_HEADERS = (
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "range",
    )
    CORS_ALLOW_CREDENTIALS = True
    SECURE_HSTS_SECONDS = 60
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", PROTOCOL)
    CSRF_TRUSTED_ORIGINS = [DOMAIN]
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "<noreply@example.com>"
    CORS_ORIGIN_WHITELIST = ["https://example.com"]
