"""Shared Pydantic models for the marketplace."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class Product(BaseModel):
    """A product or service offered by a vendor."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    price: float
    category: str
    vendor_id: str
    metadata: dict = Field(default_factory=dict)


class CartItem(BaseModel):
    """An item in the shopping cart."""
    product: Product
    quantity: int = 1


class Cart(BaseModel):
    """Shopping cart for a specific vendor."""
    vendor_id: str
    items: list[CartItem] = Field(default_factory=list)

    @property
    def total(self) -> float:
        return sum(item.product.price * item.quantity for item in self.items)

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items)


class Order(BaseModel):
    """A completed order."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vendor_id: str
    items: list[CartItem]
    total: float
    status: str = "pending"  # pending, confirmed, completed, cancelled
    created_at: datetime = Field(default_factory=datetime.now)


class VendorInfo(BaseModel):
    """Information about a vendor agent."""
    id: str
    name: str
    description: str
    url: str
    skills: list[dict] = Field(default_factory=list)
    is_healthy: bool = True


class Skill(BaseModel):
    """A skill offered by a vendor agent."""
    id: str
    name: str
    description: str


class AgentCard(BaseModel):
    """A2A Agent Card for vendor discovery."""
    name: str
    description: str
    url: str
    skills: list[Skill] = Field(default_factory=list)
    capabilities: dict = Field(default_factory=lambda: {
        "streaming": False,
        "pushNotifications": False
    })
