# demo-backend-api

> Demo backend para el workshop de **QAEngineerAgent**. Producto puro — sin tests.

API REST de gestión de **productos** y **órdenes** construida con FastAPI. OpenAPI spec se auto-genera en `/openapi.json`.

## Endpoints

| Método | Path | Descripción |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/products` | Listar productos (con paginación) |
| GET | `/products/{id}` | Obtener un producto |
| POST | `/products` | Crear producto (requiere auth) |
| GET | `/orders/{id}` | Obtener una orden |
| POST | `/orders` | Crear orden (requiere auth) |

## Run local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Luego abrí http://localhost:8000/docs (Swagger UI) o http://localhost:8000/openapi.json (spec).

## Auth (mock)

Para endpoints protegidos, mandá header `Authorization: Bearer demo-token-123`. Es un token mock fijo solo para la demo.

## Tests

**Los tests no viven acá.** Son responsabilidad del repo [demo-api-testing](https://github.com/JonathanIzquierdo/demo-api-testing), gestionado por [QAEngineerAgent](https://github.com/JonathanIzquierdo/QAEngineerAgent).

Cuando se abre un PR en este repo, el agente analiza qué endpoints/schemas cambiaron y abre un PR linkeado en `demo-api-testing` con los tests correspondientes.

## Para qué sirve este repo

Es el **target** de demostración del workshop de AI in Testing. El flujo del workshop:

1. Disparar `QAEngineerAgent` apuntado a este repo → genera tests en `demo-api-testing`
2. Abrir un PR acá que cambie un schema → el agente comenta y propone tests actualizados en `demo-api-testing`
3. Si los tests fallan al correrlos, el `Healer` diagnostica y propone fix
