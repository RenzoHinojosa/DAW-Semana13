from django.db.models import Count, Sum, F
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_GET
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import ProductoFilter
from .models import Categoria, Producto
from .permissions import IsOwnerOrReadOnly
from .serializers import CategoriaSerializer, ProductoSerializer


class CategoriaViewSet(viewsets.ModelViewSet):
    """CRUD de categorías (GET/POST/PUT/PATCH/DELETE)."""

    queryset = Categoria.objects.prefetch_related("productos")
    serializer_class = CategoriaSerializer
    search_fields = ["nombre", "descripcion"]
    ordering_fields = ["nombre", "created"]

    @extend_schema(responses=ProductoSerializer(many=True))
    @action(detail=True, methods=["get"])
    def productos_activos(self, request, pk=None):
        """GET /api/categorias/{id}/productos_activos/"""
        categoria = self.get_object()
        qs = categoria.productos.filter(status=Producto.Status.ACTIVO)
        page = self.paginate_queryset(qs)
        serializer = ProductoSerializer(page, many=True, context={"request": request})
        return self.get_paginated_response(serializer.data)


class ProductoViewSet(viewsets.ModelViewSet):
    """CRUD de productos con filtrado, búsqueda, orden y paginación."""

    # select_related evita el problema N+1 al serializar categoria/owner
    queryset = Producto.objects.select_related("categoria", "owner")
    serializer_class = ProductoSerializer
    permission_classes = [  # Override justificado: regla por propietario
        *viewsets.ModelViewSet.permission_classes,
        IsOwnerOrReadOnly,
    ]
    filterset_class = ProductoFilter
    search_fields = ["nombre", "descripcion", "categoria__nombre"]
    ordering_fields = ["created", "precio", "stock", "nombre"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(responses={200: dict})
    @action(detail=False, methods=["get"])
    def estadisticas(self, request):
        """GET /api/productos/estadisticas/ -> resumen agregado en BD."""
        qs = self.filter_queryset(self.get_queryset())
        por_status = qs.values("status").annotate(total=Count("id")).order_by("status")
        valor = qs.aggregate(valor_total=Sum(F("precio") * F("stock")))["valor_total"] or 0
        return Response(
            {"total": qs.count(), "por_status": list(por_status), "valor_total": str(valor)}
        )


# --------------------------------------------------------------------- CSRF
@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    """Entrega la cookie 'csrftoken' a una SPA.

    La SPA debe reenviarla en el header X-CSRFToken en POST/PUT/PATCH/DELETE
    cuando use autenticación por sesión.
    """
    return JsonResponse({"csrfToken": get_token(request)})


@csrf_exempt  # Justificado: endpoint público, solo lectura, sin sesión ni efectos
@require_GET
def ping(request):
    return JsonResponse({"status": "ok", "servicio": "API Inventario DAW-Semana13"})
