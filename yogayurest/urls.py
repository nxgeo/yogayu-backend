from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


VERSION = f"{settings.YOGAYU_API_VERSION}/"

token_patterns = [
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(VERSION, include(token_patterns)),
    path(VERSION, include("yogalevels.urls")),
    path(VERSION, include("yogaposes.urls")),
    path(VERSION, include("users.urls")),
    path(VERSION, include("yogahistories.urls")),
]
