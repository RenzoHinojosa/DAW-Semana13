from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("categorias", views.CategoriaViewSet)
router.register("productos", views.ProductoViewSet)

urlpatterns = [
    path("", include(router.urls)),   # raíz navegable: /api/
    path("csrf/", views.csrf_token, name="csrf-token"),
    path("ping/", views.ping, name="ping"),
]
