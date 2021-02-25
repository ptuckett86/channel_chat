from .common import Common


class Dev(Common):
    DEBUG = True
    PROTOCOL = "http"
    DOMAIN = "localhost"
    ALLOWED_HOSTS = ["*"]
    INTERNAL_IPS = [DOMAIN]
    INSTALLED_APPS = Common.INSTALLED_APPS + ["django_nose", "debug_toolbar"]
    MIDDLEWARE = Common.MIDDLEWARE + ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    TEST_RUNNER = "django_nose.NoseTestSuiteRunner"
    NOSE_ARGS = [
        Common.BASE_DIR,
        # "-s",
        "--nocapture",
        "--nologcapture",
        "--with-coverage",
        "--cover-package=xenetix",
        "--with-xunit",
    ]
    LOGGING = None
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "<noreply@example.com>"
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ORIGIN_WHITELIST = ["http://localhost:4200", "http://localhost:4300"]

