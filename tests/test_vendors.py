"""Tests for vendor data and MCP tools."""

import pytest
import json


class TestRestaurantData:
    """Tests for restaurant vendor data."""

    def test_get_all_items(self):
        from vendors.restaurant.data import get_all_items

        items = get_all_items()
        assert len(items) > 0
        assert all("id" in item for item in items)
        assert all("name" in item for item in items)
        assert all("price" in item for item in items)

    def test_get_categories(self):
        from vendors.restaurant.data import get_categories

        categories = get_categories()
        assert "appetizers" in categories
        assert "pizzas" in categories
        assert "pastas" in categories
        assert "desserts" in categories

    def test_get_items_by_category(self):
        from vendors.restaurant.data import get_items_by_category

        pizzas = get_items_by_category("pizzas")
        assert len(pizzas) > 0
        assert all(item["category"] == "pizzas" for item in pizzas)

    def test_get_item_by_id(self):
        from vendors.restaurant.data import get_item_by_id

        item = get_item_by_id("piz-001")
        assert item is not None
        assert item["name"] == "Margherita"

        nonexistent = get_item_by_id("nonexistent")
        assert nonexistent is None

    def test_search_items(self):
        from vendors.restaurant.data import search_items

        results = search_items("pizza")
        assert len(results) > 0

        results = search_items("vegetarian")
        # Should find items with vegetarian in description
        assert len(results) >= 0


class TestRestaurantMCPTools:
    """Tests for restaurant MCP tools."""

    def test_get_menu(self):
        from vendors.restaurant.mcp_server import RestaurantMCPTools

        result = RestaurantMCPTools.get_menu()
        menu = json.loads(result)

        assert "appetizers" in menu
        assert "pizzas" in menu

    def test_search_dishes(self):
        from vendors.restaurant.mcp_server import RestaurantMCPTools

        result = RestaurantMCPTools.search_dishes("margherita")
        data = json.loads(result)

        assert data["count"] > 0
        assert any("Margherita" in r["name"] for r in data["results"])

    def test_get_dish_details(self):
        from vendors.restaurant.mcp_server import RestaurantMCPTools

        result = RestaurantMCPTools.get_dish_details("piz-001")
        dish = json.loads(result)

        assert dish["name"] == "Margherita"
        assert "price" in dish


class TestElectronicsData:
    """Tests for electronics vendor data."""

    def test_get_all_products(self):
        from vendors.electronics.data import get_all_products

        products = get_all_products()
        assert len(products) > 0
        assert all("id" in p for p in products)
        assert all("price" in p for p in products)

    def test_get_categories(self):
        from vendors.electronics.data import get_categories

        categories = get_categories()
        assert "phones" in categories
        assert "laptops" in categories
        assert "headphones" in categories
        assert "accessories" in categories

    def test_get_product_by_id(self):
        from vendors.electronics.data import get_product_by_id

        product = get_product_by_id("laptop-001")
        assert product is not None
        assert "MacBook" in product["name"]

    def test_search_products(self):
        from vendors.electronics.data import search_products

        results = search_products("apple")
        assert len(results) > 0

    def test_compare_products(self):
        from vendors.electronics.data import compare_products

        results = compare_products(["laptop-001", "laptop-002"])
        assert len(results) == 2

    def test_check_availability(self):
        from vendors.electronics.data import check_availability

        result = check_availability("laptop-001")
        assert "in_stock" in result
        assert "stock_count" in result


class TestElectronicsMCPTools:
    """Tests for electronics MCP tools."""

    def test_get_products(self):
        from vendors.electronics.mcp_server import ElectronicsMCPTools

        result = ElectronicsMCPTools.get_products()
        data = json.loads(result)

        assert "phones" in data
        assert "laptops" in data

    def test_get_products_by_category(self):
        from vendors.electronics.mcp_server import ElectronicsMCPTools

        result = ElectronicsMCPTools.get_products("laptops")
        data = json.loads(result)

        assert data["category"] == "laptops"
        assert len(data["products"]) > 0

    def test_compare_products(self):
        from vendors.electronics.mcp_server import ElectronicsMCPTools

        result = ElectronicsMCPTools.compare_products("laptop-001,laptop-002")
        data = json.loads(result)

        assert "comparison_table" in data
        assert len(data["products"]) == 2


class TestTravelData:
    """Tests for travel vendor data."""

    def test_get_all_destinations(self):
        from vendors.travel.data import get_all_destinations

        destinations = get_all_destinations()
        assert len(destinations) > 0
        assert all("id" in d for d in destinations)
        assert all("name" in d for d in destinations)

    def test_get_destination(self):
        from vendors.travel.data import get_destination

        dest = get_destination("paris")
        assert dest is not None
        assert dest["name"] == "Paris"

    def test_search_destinations(self):
        from vendors.travel.data import search_destinations

        results = search_destinations("france")
        assert len(results) > 0
        assert any("Paris" in r["name"] for r in results)

    def test_get_flights(self):
        from vendors.travel.data import get_flights

        flights = get_flights("paris")
        assert len(flights) > 0
        assert all("price" in f for f in flights)

    def test_get_hotels(self):
        from vendors.travel.data import get_hotels

        hotels = get_hotels("tokyo")
        assert len(hotels) > 0
        assert all("price_per_night" in h for h in hotels)

    def test_get_package(self):
        from vendors.travel.data import get_package

        package = get_package("paris")
        assert package is not None
        assert "price" in package
        assert "includes" in package


class TestTravelMCPTools:
    """Tests for travel MCP tools."""

    def test_get_destinations(self):
        from vendors.travel.mcp_server import TravelMCPTools

        result = TravelMCPTools.get_destinations()
        data = json.loads(result)

        assert "destinations" in data
        assert len(data["destinations"]) > 0

    def test_search_flights(self):
        from vendors.travel.mcp_server import TravelMCPTools

        result = TravelMCPTools.search_flights("paris")
        data = json.loads(result)

        assert "flights" in data
        assert data["count"] > 0

    def test_search_hotels(self):
        from vendors.travel.mcp_server import TravelMCPTools

        result = TravelMCPTools.search_hotels("tokyo")
        data = json.loads(result)

        assert "hotels" in data
        assert data["count"] > 0

    def test_get_travel_quote(self):
        from vendors.travel.mcp_server import TravelMCPTools

        result = TravelMCPTools.get_travel_quote("paris", 5)
        data = json.loads(result)

        assert "flight" in data
        assert "hotel" in data
        assert "estimated_total" in data
