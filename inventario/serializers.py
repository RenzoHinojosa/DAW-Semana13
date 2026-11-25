from decimal import Decimal

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Categoria, Producto


class CategoriaSerializer(serializers.HyperlinkedModelSerializer):
    """Representación hipervinculada (HATEOAS): enlaces en lugar de IDs."""

    url = serializers.HyperlinkedIdentityField(view_name="categoria-detail")
    productos = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="producto-detail"
    )
    total_productos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ("url", "id", "nombre", "descripcion", "total_productos", "productos", "created")
        read_only_fields = ("created",)

    def get_total_productos(self, obj) -> int:
        return obj.productos.count()


class ProductoSerializer(serializers.ModelSerializer):
    """Serializador explícito (nunca __all__) con campos de solo lectura."""

    url = serializers.HyperlinkedIdentityField(view_name="producto-detail")
    owner = serializers.ReadOnlyField(source="owner.username")
    categoria_nombre = serializers.ReadOnlyField(source="categoria.nombre")
    valor_inventario = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = (
            "url", "id", "nombre", "descripcion", "precio", "stock", "status",
            "categoria", "categoria_nombre", "owner", "valor_inventario",
            "links", "created", "updated",
        )
        read_only_fields = ("created", "updated")

    # ---- campos calculados -------------------------------------------------
    def get_valor_inventario(self, obj) -> str:
        return str(obj.precio * obj.stock)

    def get_links(self, obj) -> dict:
        """HATEOAS básico: la propia respuesta indica cómo navegar."""
        request = self.context.get("request")
        return {
            "self": reverse("producto-detail", args=[obj.pk], request=request),
            "categoria": reverse("categoria-detail", args=[obj.categoria_id], request=request),
            "coleccion": reverse("producto-list", request=request),
        }

    # ---- validación --------------------------------------------------------
    def validate_precio(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError("El precio debe ser mayor que 0.")
        return value

    def validate_nombre(self, value):
        return value.strip()

    def validate(self, attrs):
        """Validación cruzada entre campos (stock vs status)."""
        # En PATCH, completar con los valores actuales de la instancia
        stock = attrs.get("stock", getattr(self.instance, "stock", 0))
        status = attrs.get("status", getattr(self.instance, "status", Producto.Status.ACTIVO))

        if status == Producto.Status.AGOTADO and stock > 0:
            raise serializers.ValidationError(
                {"status": "Un producto con stock > 0 no puede estar 'agotado'."}
            )
        if status == Producto.Status.ACTIVO and stock == 0:
            raise serializers.ValidationError(
                {"status": "Un producto activo debe tener stock; use 'agotado'."}
            )
        return attrs
