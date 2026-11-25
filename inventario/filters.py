import django_filters

from .models import Producto


class ProductoFilter(django_filters.FilterSet):
    """Ej.: /api/productos/?status=activo&precio_min=5&stock_max=10"""

    precio_min = django_filters.NumberFilter(field_name="precio", lookup_expr="gte")
    precio_max = django_filters.NumberFilter(field_name="precio", lookup_expr="lte")
    stock_max = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")
    creado_desde = django_filters.DateFilter(field_name="created", lookup_expr="date__gte")

    class Meta:
        model = Producto
        fields = ["status", "categoria", "owner"]
