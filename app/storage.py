"""
In-memory storage for the demo.
In a real app this would be a database — the agent only cares about the API surface.
"""
from datetime import datetime, timezone
from typing import Optional
import uuid

from app.schemas import Product, Order, OrderItem


# In-memory stores
_products: dict[str, Product] = {}
_orders: dict[str, Order] = {}


# Seed a few products so GET /products is not empty
def _seed():
    for name, sku, price, stock in [
        ("Wireless Mouse", "MOUSE-001", 25.99, 50),
        ("Mechanical Keyboard", "KEYB-002", 89.50, 20),
        ("USB-C Hub", "HUB-003", 35.00, 100),
    ]:
        pid = str(uuid.uuid4())
        _products[pid] = Product(
            id=pid,
            name=name,
            sku=sku,
            price=price,
            stock=stock,
            created_at=datetime.now(timezone.utc),
        )


_seed()


# -------- Products --------

def list_products(limit: int = 20, offset: int = 0) -> list[Product]:
    return list(_products.values())[offset:offset + limit]


def get_product(product_id: str) -> Optional[Product]:
    return _products.get(product_id)


def create_product(name: str, sku: str, price: float, stock: int) -> Product:
    # Enforce SKU uniqueness
    for p in _products.values():
        if p.sku == sku:
            raise ValueError(f"SKU '{sku}' already exists")
    pid = str(uuid.uuid4())
    product = Product(
        id=pid,
        name=name,
        sku=sku,
        price=price,
        stock=stock,
        created_at=datetime.now(timezone.utc),
    )
    _products[pid] = product
    return product


# -------- Orders --------

def get_order(order_id: str) -> Optional[Order]:
    return _orders.get(order_id)


def create_order(customer_email: str, items: list[OrderItem]) -> Order:
    # Validate products exist and compute total
    total = 0.0
    for item in items:
        product = _products.get(item.product_id)
        if not product:
            raise ValueError(f"Product not found: {item.product_id}")
        total += product.price * item.quantity

    oid = str(uuid.uuid4())
    order = Order(
        id=oid,
        customer_email=customer_email,
        items=items,
        total=round(total, 2),
        status="pending",
        created_at=datetime.now(timezone.utc),
    )
    _orders[oid] = order
    return order
