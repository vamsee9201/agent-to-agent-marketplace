"""Tests for cart management."""

import pytest
from concierge.cart import CartManager, CartItem, Order


@pytest.fixture
def cart():
    """Create a fresh cart for testing."""
    return CartManager()


@pytest.fixture
def sample_item():
    """Create a sample cart item."""
    return {
        "name": "Margherita Pizza",
        "price": 14.99,
        "vendor_id": "http://localhost:10001",
        "vendor_name": "Bella's Italian Restaurant",
        "quantity": 1,
        "description": "Classic pizza"
    }


class TestCartManager:
    """Tests for CartManager class."""

    def test_init(self, cart):
        """Test cart initialization."""
        assert len(cart.items) == 0
        assert len(cart.orders) == 0
        assert cart.total == 0
        assert cart.item_count == 0

    def test_add_item(self, cart, sample_item):
        """Test adding item to cart."""
        item = cart.add_item(**sample_item)

        assert isinstance(item, CartItem)
        assert item.name == "Margherita Pizza"
        assert item.price == 14.99
        assert len(cart.items) == 1
        assert cart.total == 14.99

    def test_add_multiple_items(self, cart, sample_item):
        """Test adding multiple items."""
        cart.add_item(**sample_item)
        cart.add_item(
            name="Tiramisu",
            price=8.99,
            vendor_id="http://localhost:10001",
            vendor_name="Bella's Italian Restaurant"
        )

        assert len(cart.items) == 2
        assert cart.total == pytest.approx(23.98, 0.01)

    def test_add_item_with_quantity(self, cart, sample_item):
        """Test adding item with quantity."""
        sample_item["quantity"] = 3
        cart.add_item(**sample_item)

        assert cart.item_count == 3
        assert cart.total == pytest.approx(44.97, 0.01)

    def test_remove_item(self, cart, sample_item):
        """Test removing item from cart."""
        item = cart.add_item(**sample_item)

        assert len(cart.items) == 1
        result = cart.remove_item(item.id)

        assert result is True
        assert len(cart.items) == 0

    def test_remove_nonexistent_item(self, cart):
        """Test removing item that doesn't exist."""
        result = cart.remove_item("nonexistent-id")
        assert result is False

    def test_update_quantity(self, cart, sample_item):
        """Test updating item quantity."""
        item = cart.add_item(**sample_item)

        result = cart.update_quantity(item.id, 5)

        assert result is True
        assert cart.items[0].quantity == 5
        assert cart.total == pytest.approx(74.95, 0.01)

    def test_update_quantity_to_zero_removes(self, cart, sample_item):
        """Test that updating quantity to 0 removes item."""
        item = cart.add_item(**sample_item)

        result = cart.update_quantity(item.id, 0)

        assert result is True
        assert len(cart.items) == 0

    def test_clear_cart(self, cart, sample_item):
        """Test clearing the cart."""
        cart.add_item(**sample_item)
        cart.add_item(name="Test", price=10, vendor_id="v1", vendor_name="V1")

        cart.clear()

        assert len(cart.items) == 0
        assert cart.total == 0

    def test_get_items_by_vendor(self, cart):
        """Test getting items by vendor."""
        cart.add_item(
            name="Pizza",
            price=15,
            vendor_id="http://localhost:10001",
            vendor_name="Restaurant"
        )
        cart.add_item(
            name="Laptop",
            price=999,
            vendor_id="http://localhost:10002",
            vendor_name="Electronics"
        )

        restaurant_items = cart.get_items_by_vendor("http://localhost:10001")

        assert len(restaurant_items) == 1
        assert restaurant_items[0].name == "Pizza"

    def test_get_summary(self, cart):
        """Test getting cart summary."""
        cart.add_item(
            name="Pizza",
            price=15,
            vendor_id="http://localhost:10001",
            vendor_name="Restaurant"
        )
        cart.add_item(
            name="Laptop",
            price=999,
            vendor_id="http://localhost:10002",
            vendor_name="Electronics"
        )

        summary = cart.get_summary()

        assert "vendors" in summary
        assert len(summary["vendors"]) == 2
        assert summary["item_count"] == 2
        assert summary["total"] == 1014

    def test_format_cart_empty(self, cart):
        """Test formatting empty cart."""
        output = cart.format_cart()
        assert "empty" in output.lower()

    def test_format_cart_with_items(self, cart, sample_item):
        """Test formatting cart with items."""
        cart.add_item(**sample_item)

        output = cart.format_cart()

        assert "Shopping Cart" in output
        assert "Margherita Pizza" in output
        assert "Bella's Italian Restaurant" in output

    def test_checkout_empty_cart(self, cart):
        """Test checkout with empty cart."""
        orders = cart.checkout()
        assert len(orders) == 0

    def test_checkout_single_vendor(self, cart, sample_item):
        """Test checkout with single vendor."""
        cart.add_item(**sample_item)

        orders = cart.checkout()

        assert len(orders) == 1
        assert orders[0].vendor_name == "Bella's Italian Restaurant"
        assert orders[0].total == 14.99
        assert orders[0].status == "confirmed"
        assert len(cart.items) == 0  # Cart cleared

    def test_checkout_multiple_vendors(self, cart):
        """Test checkout with multiple vendors."""
        cart.add_item(
            name="Pizza",
            price=15,
            vendor_id="http://localhost:10001",
            vendor_name="Restaurant"
        )
        cart.add_item(
            name="Laptop",
            price=999,
            vendor_id="http://localhost:10002",
            vendor_name="Electronics"
        )

        orders = cart.checkout()

        assert len(orders) == 2
        assert len(cart.items) == 0
        assert len(cart.orders) == 2

    def test_format_orders(self, cart, sample_item):
        """Test formatting orders."""
        cart.add_item(**sample_item)
        orders = cart.checkout()

        output = cart.format_orders(orders)

        assert "Orders Confirmed" in output
        assert "Bella's Italian Restaurant" in output
        assert "confirmed" in output
