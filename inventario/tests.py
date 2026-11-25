from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Categoria, Producto

User = get_user_model()


class ApiProductoTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("ana", password="pass12345")
        self.otro = User.objects.create_user("beto", password="pass12345")
        self.cat = Categoria.objects.create(nombre="Test")
        for i in range(7):
            Producto.objects.create(
                nombre=f"P{i}", precio=10 + i, stock=i, status="activo" if i else "agotado",
                categoria=self.cat, owner=self.user,
            )

    def test_lista_publica_y_paginada(self):
        r = self.client.get("/api/productos/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data["count"], 7)
        self.assertEqual(len(r.data["results"]), 5)
        self.assertIn("links", r.data["results"][0])  # HATEOAS

    def test_filtro_y_orden(self):
        r = self.client.get("/api/productos/?status=agotado")
        self.assertEqual(r.data["count"], 1)
        r = self.client.get("/api/productos/?ordering=precio&precio_min=14")
        self.assertEqual(r.data["results"][0]["nombre"], "P4")

    def test_busqueda(self):
        r = self.client.get("/api/productos/?search=P3")
        self.assertEqual(r.data["count"], 1)

    def test_crear_requiere_auth(self):
        data = {"nombre": "X", "precio": "5.00", "stock": 3, "status": "activo", "categoria": self.cat.id}
        self.assertEqual(self.client.post("/api/productos/", data).status_code, 403)
        self.client.force_authenticate(self.user)
        r = self.client.post("/api/productos/", data)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data["owner"], "ana")

    def test_validacion_cruzada(self):
        self.client.force_authenticate(self.user)
        data = {"nombre": "X", "precio": "5.00", "stock": 0, "status": "activo", "categoria": self.cat.id}
        self.assertEqual(self.client.post("/api/productos/", data).status_code, 400)
        data.update(precio="-1", stock=2)
        self.assertEqual(self.client.post("/api/productos/", data).status_code, 400)

    def test_solo_propietario_modifica(self):
        p = Producto.objects.filter(status="activo").first()
        self.client.force_authenticate(self.otro)
        self.assertEqual(self.client.patch(f"/api/productos/{p.id}/", {"precio": "99"}).status_code, 403)
        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.patch(f"/api/productos/{p.id}/", {"precio": "99"}).status_code, 200)

    def test_estadisticas_y_ping(self):
        r = self.client.get("/api/productos/estadisticas/")
        self.assertEqual(r.data["total"], 7)
        self.assertEqual(self.client.get("/api/ping/").json()["status"], "ok")

    def test_categoria_hipervinculada(self):
        r = self.client.get("/api/categorias/")
        self.assertTrue(r.data["results"][0]["url"].startswith("http"))
        self.assertEqual(self.client.get(f"/api/categorias/{self.cat.id}/productos_activos/").status_code, 200)

    def test_openapi(self):
        self.assertEqual(self.client.get("/api/schema/").status_code, 200)
        self.assertEqual(self.client.get("/api/docs/").status_code, 200)
