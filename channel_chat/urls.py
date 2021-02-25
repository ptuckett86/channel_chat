"""channel_chat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView

from rest_framework_jwt.views import (
    obtain_jwt_token,
    refresh_jwt_token,
    verify_jwt_token,
)

from core.views import *

from .routes import router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/login/", login_obtain_jwt_token),
    path("api/v1/auth/refresh_token/", refresh_jwt_token),
    path("api/v1/auth/verify_token/", verify_jwt_token),
    path("api/v1/auth/activate_email/resend", ResendEmailConfirmToken.as_view()),
    re_path(
        "api/v1/auth/activate_email/confirm/(?P<token>.*)/", EmailConfirmView.as_view()
    ),
    path("api/v1/auth/password_reset/resend/", ObtainEmailPasswordResetToken.as_view()),
    re_path(
        "api/v1/auth/password_reset/confirm/(?P<token>.*)/", PasswordResetView.as_view()
    ),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
