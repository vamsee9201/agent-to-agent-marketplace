"""Tests for vendor discovery."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx

from concierge.discovery import VendorRegistry, VendorInfo


@pytest.fixture
def registry():
    """Create a fresh registry for testing."""
    return VendorRegistry(vendor_urls=[
        "http://localhost:10001",
        "http://localhost:10002",
        "http://localhost:10003",
    ])


@pytest.fixture
def mock_agent_cards():
    """Mock agent card responses."""
    return {
        "http://localhost:10001": {
            "name": "Bella's Italian Restaurant",
            "description": "Italian restaurant with pizza and pasta",
            "skills": [{"id": "browse_menu", "name": "Browse Menu", "description": "View menu"}]
        },
        "http://localhost:10002": {
            "name": "TechZone Electronics",
            "description": "Consumer electronics store",
            "skills": [{"id": "browse_products", "name": "Browse Products", "description": "View products"}]
        },
        "http://localhost:10003": {
            "name": "Wanderlust Travel",
            "description": "Travel booking service",
            "skills": [{"id": "search_destinations", "name": "Search Destinations", "description": "Find destinations"}]
        }
    }


class TestVendorRegistry:
    """Tests for VendorRegistry class."""

    def test_init(self, registry):
        """Test registry initialization."""
        assert len(registry.vendor_urls) == 3
        assert len(registry.vendors) == 0
        assert not registry._discovered

    @pytest.mark.asyncio
    async def test_discover_all_success(self, registry, mock_agent_cards):
        """Test successful vendor discovery."""
        async def mock_get(url):
            base_url = url.rsplit("/.well-known", 1)[0]
            if base_url in mock_agent_cards:
                response = MagicMock()
                response.status_code = 200
                response.json.return_value = mock_agent_cards[base_url]
                return response
            raise httpx.HTTPError("Not found")

        with patch("httpx.AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.get = mock_get
            mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
            mock_instance.__aexit__ = AsyncMock(return_value=None)
            mock_client.return_value = mock_instance

            vendors = await registry.discover_all()

            assert len(vendors) == 3
            assert registry._discovered

    def test_find_vendors_for_intent_food(self, registry):
        """Test finding vendors for food-related intent."""
        # Add mock vendors
        registry.vendors = {
            "http://localhost:10001": VendorInfo(
                name="Bella's Italian Restaurant",
                description="Italian food",
                url="http://localhost:10001",
                skills=[{"id": "browse_menu", "name": "Browse Menu"}]
            )
        }

        matches = registry.find_vendors_for_intent("I want pizza")
        assert len(matches) == 1
        assert matches[0].name == "Bella's Italian Restaurant"

    def test_find_vendors_for_intent_electronics(self, registry):
        """Test finding vendors for electronics-related intent."""
        registry.vendors = {
            "http://localhost:10002": VendorInfo(
                name="TechZone Electronics",
                description="Electronics store",
                url="http://localhost:10002",
                skills=[]
            )
        }

        matches = registry.find_vendors_for_intent("I need a new laptop")
        assert len(matches) == 1

    def test_get_vendor_by_name(self, registry):
        """Test getting vendor by name."""
        registry.vendors = {
            "http://localhost:10001": VendorInfo(
                name="Bella's Italian Restaurant",
                description="Italian food",
                url="http://localhost:10001"
            )
        }

        vendor = registry.get_vendor_by_name("bella")
        assert vendor is not None
        assert vendor.name == "Bella's Italian Restaurant"

        vendor = registry.get_vendor_by_name("nonexistent")
        assert vendor is None

    def test_format_vendors_list(self, registry):
        """Test formatting vendors list."""
        registry.vendors = {
            "http://localhost:10001": VendorInfo(
                name="Test Vendor",
                description="A test vendor",
                url="http://localhost:10001",
                skills=[{"name": "Skill 1"}, {"name": "Skill 2"}],
                is_healthy=True
            )
        }

        output = registry.format_vendors_list()
        assert "Test Vendor" in output
        assert "A test vendor" in output
        assert "Skill 1" in output

    def test_get_all_healthy_vendors(self, registry):
        """Test getting healthy vendors only."""
        registry.vendors = {
            "http://localhost:10001": VendorInfo(
                name="Healthy Vendor",
                description="Online",
                url="http://localhost:10001",
                is_healthy=True
            ),
            "http://localhost:10002": VendorInfo(
                name="Unhealthy Vendor",
                description="Offline",
                url="http://localhost:10002",
                is_healthy=False
            )
        }

        healthy = registry.get_all_healthy_vendors()
        assert len(healthy) == 1
        assert healthy[0].name == "Healthy Vendor"
