"""
Schemas (Pydantic) for products and orders.
These auto-generate the OpenAPI spec at /openapi.json.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# -------- Products --------

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    sku: str = Field(..., pattern=r"^[A-Z0-9-]{4,20}$", description="Stock keeping unit")
    price: float = Field(..., gt=0, description="Price in USD")
    stock: int = Field(default=0, ge=0, description="Units in stock")


class Product(ProductCreate):
    id: str
    created_at: datetime


# -------- Orders --------

class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_email: str = Field(..., description="Customer email address")
    items: list[OrderItem] = Field(..., min_length=1)


class Order(BaseModel):
    id: str
    customer_email: str
    items: list[OrderItem]
    total: float
    status: str = Field(..., description="Order status: pending|paid|shipped|cancelled")
    created_at: datetime


# -------- Errors --------

class ErrorResponse(BaseModel):
    detail: str
