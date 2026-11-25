from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="inventario/dashboard.html"), name="inicio"),
    path("admin/", admin.site.urls),
    path("api/", include("inventario.urls")),
    # Documentación OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    # Login/logout de la API navegable (sesión)
    path("api-auth/", include("rest_framework.urls")),
]
