import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from inventario.models import Categoria, Producto

DATOS = {
    "Abarrotes": ["Arroz costeño 1kg", "Azúcar rubia 1kg", "Aceite vegetal 1L", "Fideos spaghetti", "Lentejas 500g"],
    "Bebidas": ["Gaseosa 2L", "Agua mineral 625ml", "Jugo de naranja 1L", "Cerveza 620ml"],
    "Limpieza": ["Detergente 1kg", "Lejía 1L", "Jabón de ropa", "Esponja multiuso"],
    "Lácteos": ["Leche evaporada", "Yogurt 1L", "Queso fresco", "Mantequilla 200g"],
}


class Command(BaseCommand):
    help = "Crea usuarios de prueba, categorías y productos de ejemplo."

    def handle(self, *args, **options):
        User = get_user_model()
        admin, _ = User.objects.get_or_create(
            username="admin", defaults={"is_staff": True, "is_superuser": True, "email": "admin@example.com"}
        )
        admin.set_password("admin12345")
        admin.save()
        demo, _ = User.objects.get_or_create(username="demo")
        demo.set_password("demo12345")
        demo.save()

        random.seed(13)
        if Producto.objects.exists():
            self.stdout.write("Ya existen productos; no se vuelve a sembrar.")
        else:
            for nombre_cat, productos in DATOS.items():
                cat, _ = Categoria.objects.get_or_create(
                    nombre=nombre_cat, defaults={"descripcion": f"Productos de {nombre_cat.lower()}"}
                )
                for nombre in productos:
                    stock = random.choice([0, 3, 8, 15, 40, 100])
                    Producto.objects.create(
                        nombre=nombre,
                        descripcion=f"{nombre} - producto de ejemplo",
                        precio=round(random.uniform(2, 60), 2),
                        stock=stock,
                        status="agotado" if stock == 0 else random.choice(["activo", "activo", "inactivo"]),
                        categoria=cat,
                        owner=random.choice([admin, demo]),
                    )
        self.stdout.write(self.style.SUCCESS(
            "Listo. Usuarios: admin/admin12345 (staff) y demo/demo12345."
        ))
