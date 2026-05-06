"""
FastAPI app exposing the demo backend.

OpenAPI spec is auto-generated and exposed at /openapi.json.
The QAEngineerAgent reads this spec to discover endpoints and schemas.
"""
from fastapi import FastAPI, HTTPException, Header, status, Query
from fastapi.responses import JSONResponse

from app import storage
from app.schemas import (
    Product,
    ProductCreate,
    Order,
    OrderCreate,
    ErrorResponse,
)


app = FastAPI(
    title="demo-backend-api",
    version="1.0.0",
    description="Demo backend for the QAEngineerAgent workshop.",
)


# -------- Auth helper (mock) --------

DEMO_TOKEN = "demo-token-123"


def require_auth(authorization: str | None) -> None:
    """Mock auth: accept only the fixed demo token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.removeprefix("Bearer ").strip()
    if token != DEMO_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")


# -------- Health --------

@app.get("/health", tags=["health"])
def health():
    """Health check endpoint."""
    return {"status": "ok"}


# -------- Products --------

@app.get(
    "/products",
    response_model=list[Product],
    tags=["products"],
    summary="List products",
)
def list_products(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Returns a paginated list of products."""
    return storage.list_products(limit=limit, offset=offset)


@app.get(
    "/products/{product_id}",
    response_model=Product,
    responses={404: {"model": ErrorResponse}},
    tags=["products"],
    summary="Get product by ID",
)
def get_product(product_id: str):
    product = storage.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post(
    "/products",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
    tags=["products"],
    summary="Create a new product",
)
def create_product(
    payload: ProductCreate,
    authorization: str | None = Header(default=None),
):
    """Creates a new product. Requires authentication."""
    require_auth(authorization)
    try:
        return storage.create_product(
            name=payload.name,
            sku=payload.sku,
            price=payload.price,
            stock=payload.stock,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


# -------- Orders --------

@app.get(
    "/orders/{order_id}",
    response_model=Order,
    responses={404: {"model": ErrorResponse}},
    tags=["orders"],
    summary="Get order by ID",
)
def get_order(order_id: str):
    order = storage.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post(
    "/orders",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
    tags=["orders"],
    summary="Create a new order",
)
def create_order(
    payload: OrderCreate,
    authorization: str | None = Header(default=None),
):
    """Creates a new order. Requires authentication."""
    require_auth(authorization)
    try:
        return storage.create_order(
            customer_email=payload.customer_email,
            items=payload.items,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
