"""Cart management for the Purchasing Concierge."""

from typing import Optional
from pydantic import BaseModel, Field
import uuid
from datetime import datetime


class CartItem(BaseModel):
    """An item in the shopping cart."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    price: float
    quantity: int = 1
    vendor_id: str
    vendor_name: str
    metadata: dict = Field(default_factory=dict)


class Order(BaseModel):
    """A completed order."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vendor_id: str
    vendor_name: str
    items: list[CartItem]
    total: float
    status: str = "confirmed"
    created_at: datetime = Field(default_factory=datetime.now)


class CartManager:
    """Unified cart across multiple vendors."""

    def __init__(self):
        self.items: list[CartItem] = []
        self.orders: list[Order] = []

    def add_item(
        self,
        name: str,
        price: float,
        vendor_id: str,
        vendor_name: str,
        quantity: int = 1,
        description: str = "",
        metadata: dict = None
    ) -> CartItem:
        """Add an item to the cart."""
        item = CartItem(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            vendor_id=vendor_id,
            vendor_name=vendor_name,
            metadata=metadata or {}
        )
        self.items.append(item)
        return item

    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the cart by ID."""
        for i, item in enumerate(self.items):
            if item.id == item_id:
                self.items.pop(i)
                return True
        return False

    def update_quantity(self, item_id: str, quantity: int) -> bool:
        """Update the quantity of an item."""
        for item in self.items:
            if item.id == item_id:
                if quantity <= 0:
                    return self.remove_item(item_id)
                item.quantity = quantity
                return True
        return False

    def clear(self):
        """Clear all items from the cart."""
        self.items = []

    def get_items_by_vendor(self, vendor_id: str) -> list[CartItem]:
        """Get all items from a specific vendor."""
        return [item for item in self.items if item.vendor_id == vendor_id]

    @property
    def total(self) -> float:
        """Get the total cart value."""
        return sum(item.price * item.quantity for item in self.items)

    @property
    def item_count(self) -> int:
        """Get the total number of items."""
        return sum(item.quantity for item in self.items)

    def get_summary(self) -> dict:
        """Get a summary of the cart."""
        # Group by vendor
        vendors = {}
        for item in self.items:
            if item.vendor_name not in vendors:
                vendors[item.vendor_name] = {
                    "items": [],
                    "subtotal": 0.0
                }
            vendors[item.vendor_name]["items"].append({
                "name": item.name,
                "quantity": item.quantity,
                "price": item.price,
                "line_total": item.price * item.quantity
            })
            vendors[item.vendor_name]["subtotal"] += item.price * item.quantity

        return {
            "vendors": vendors,
            "item_count": self.item_count,
            "total": self.total
        }

    def format_cart(self) -> str:
        """Format the cart for display."""
        if not self.items:
            return "Your cart is empty."

        lines = ["🛒 Shopping Cart", "=" * 40]
        summary = self.get_summary()

        for vendor_name, vendor_data in summary["vendors"].items():
            lines.append(f"\n📦 {vendor_name}")
            lines.append("-" * 30)
            for item in vendor_data["items"]:
                lines.append(
                    f"  • {item['name']} x{item['quantity']} "
                    f"@ ${item['price']:.2f} = ${item['line_total']:.2f}"
                )
            lines.append(f"  Subtotal: ${vendor_data['subtotal']:.2f}")

        lines.append("\n" + "=" * 40)
        lines.append(f"Total Items: {summary['item_count']}")
        lines.append(f"Grand Total: ${summary['total']:.2f}")

        return "\n".join(lines)

    def checkout(self) -> list[Order]:
        """Complete the checkout and create orders."""
        if not self.items:
            return []

        # Group items by vendor
        vendor_items: dict[str, list[CartItem]] = {}
        for item in self.items:
            if item.vendor_id not in vendor_items:
                vendor_items[item.vendor_id] = []
            vendor_items[item.vendor_id].append(item)

        # Create an order for each vendor
        orders = []
        for vendor_id, items in vendor_items.items():
            vendor_name = items[0].vendor_name
            total = sum(item.price * item.quantity for item in items)

            order = Order(
                vendor_id=vendor_id,
                vendor_name=vendor_name,
                items=items.copy(),
                total=total
            )
            orders.append(order)
            self.orders.append(order)

        # Clear the cart
        self.clear()

        return orders

    def format_orders(self, orders: list[Order]) -> str:
        """Format orders for display."""
        if not orders:
            return "No orders created."

        lines = ["✅ Orders Confirmed!", "=" * 40]

        for order in orders:
            lines.append(f"\n📋 Order #{order.id[:8]}")
            lines.append(f"   Vendor: {order.vendor_name}")
            lines.append(f"   Status: {order.status}")
            lines.append(f"   Items:")
            for item in order.items:
                lines.append(f"     • {item.name} x{item.quantity}")
            lines.append(f"   Total: ${order.total:.2f}")
            lines.append(f"   Created: {order.created_at.strftime('%Y-%m-%d %H:%M')}")

        return "\n".join(lines)


# Singleton cart instance
_cart: Optional[CartManager] = None


def get_cart() -> CartManager:
    """Get the global cart instance."""
    global _cart
    if _cart is None:
        _cart = CartManager()
    return _cart
