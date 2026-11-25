# DAW-Semana13 — API RESTful con Django REST Framework

Asignatura: Desarrollo de Aplicaciones Web (IS093A) — UNCP.
Serialización, ViewSets, Routers, paginación, filtrado, throttling, CORS/CSRF, HATEOAS y OpenAPI.

## Ejecutar en Visual Studio Code (Windows / PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py check
python manage.py runserver
```

> Si PowerShell bloquea el script: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.
> En Linux/macOS: `source .venv/bin/activate`.
> En VS Code: `Ctrl+Shift+P` → *Python: Select Interpreter* → elija `.venv`.

## URLs

| URL | Descripción |
|---|---|
| http://127.0.0.1:8000/api/ | Raíz navegable (HATEOAS) |
| http://127.0.0.1:8000/api/productos/ | CRUD de productos |
| http://127.0.0.1:8000/api/categorias/ | CRUD de categorías |
| http://127.0.0.1:8000/api/docs/ | Swagger UI |
| http://127.0.0.1:8000/api/redoc/ | ReDoc |
| http://127.0.0.1:8000/api/schema/ | Esquema OpenAPI 3 |
| http://127.0.0.1:8000/admin/ | Admin de Django |

Usuarios de prueba (`python manage.py seed`): `admin / admin12345` (staff), `demo / demo12345`.

## Query params

`?status=activo&categoria=1&precio_min=5&precio_max=50&stock_max=20&search=arroz&ordering=-created&page=2`

## Pruebas

```powershell
python manage.py test
python manage.py spectacular --file schema.yml
```

Para pruebas HTTP abra `requests.http` (extensión REST Client).

## Qué cubre cada fase de la guía

1. **Setup**: `config/settings.py` (INSTALLED_APPS, REST_FRAMEWORK, CORS, SPECTACULAR_SETTINGS).
2. **Serialización**: `inventario/serializers.py` (ModelSerializer, HyperlinkedModelSerializer, ReadOnlyField, SerializerMethodField, `validate()`).
3. **ViewSets/Routers**: `inventario/views.py`, `inventario/urls.py` (`DefaultRouter`, `@action`).
4. **Filtrado/Paginación/Throttling**: `inventario/filters.py` + `REST_FRAMEWORK` (anon 20/min, user 100/min, PAGE_SIZE 5).
5. **CORS/CSRF/Docs**: middleware `corsheaders`, `/api/csrf/` (header `X-CSRFToken`), `/api/ping/` (`@csrf_exempt` público), `/api/docs/`.

## Subir a GitHub

```powershell
git config --global user.name "RenzoHinojosa"
git config --global user.email "hinojosayarangasebastian@gmail.com"

git init
git add .
git commit -m "Semana 13: API RESTful con Django REST Framework"
git branch -M main
git remote add origin https://github.com/RenzoHinojosa/DAW-Semana13.git
git push -u origin main
```

Antes, cree el repositorio **vacío** `DAW-Semana13` en https://github.com/new (sin README, sin .gitignore).
