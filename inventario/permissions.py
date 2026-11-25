from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Lectura para todos; escritura solo del propietario o de un staff.

    Se sobrescribe el permiso global únicamente aquí porque la regla de
    negocio es específica del recurso Producto.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.owner_id == request.user.id
