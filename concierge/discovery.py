"""Vendor discovery and registry for the Purchasing Concierge."""

import asyncio
import httpx
from typing import Optional
from pydantic import BaseModel

from .config import VENDOR_URLS, DISCOVERY_TIMEOUT, HEALTH_CHECK_TIMEOUT


class VendorInfo(BaseModel):
    """Information about a discovered vendor."""
    name: str
    description: str
    url: str
    skills: list[dict] = []
    is_healthy: bool = True


class VendorRegistry:
    """Manages vendor agent discovery and health checks."""

    def __init__(self, vendor_urls: list[str] = None):
        self.vendor_urls = vendor_urls or VENDOR_URLS
        self.vendors: dict[str, VendorInfo] = {}
        self._discovered = False

    async def discover_all(self) -> dict[str, VendorInfo]:
        """Fetch agent cards from all configured vendors."""
        if self._discovered:
            return self.vendors

        async with httpx.AsyncClient(timeout=DISCOVERY_TIMEOUT) as client:
            tasks = [
                self._discover_vendor(client, url)
                for url in self.vendor_urls
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, VendorInfo):
                    self.vendors[result.url] = result

        self._discovered = True
        return self.vendors

    async def _discover_vendor(self, client: httpx.AsyncClient, url: str) -> Optional[VendorInfo]:
        """Discover a single vendor by fetching its agent card."""
        try:
            # Try the standard A2A agent card endpoint
            response = await client.get(f"{url}/.well-known/agent.json")
            if response.status_code == 200:
                card = response.json()
                return VendorInfo(
                    name=card.get("name", "Unknown"),
                    description=card.get("description", ""),
                    url=url,
                    skills=card.get("skills", []),
                    is_healthy=True
                )
        except Exception as e:
            print(f"Failed to discover vendor at {url}: {e}")
        return None

    async def health_check(self) -> dict[str, bool]:
        """Check health of all vendors."""
        results = {}
        async with httpx.AsyncClient(timeout=HEALTH_CHECK_TIMEOUT) as client:
            for url, vendor in self.vendors.items():
                try:
                    response = await client.get(f"{url}/.well-known/agent.json")
                    is_healthy = response.status_code == 200
                    vendor.is_healthy = is_healthy
                    results[url] = is_healthy
                except Exception:
                    vendor.is_healthy = False
                    results[url] = False
        return results

    def find_vendors_for_intent(self, intent: str) -> list[VendorInfo]:
        """Match user intent to vendor capabilities using keyword matching."""
        intent_lower = intent.lower()
        matches = []

        # Keyword mappings for each vendor type
        keywords = {
            "restaurant": ["food", "eat", "dinner", "lunch", "breakfast", "restaurant",
                          "pizza", "pasta", "italian", "menu", "dish", "order food",
                          "hungry", "meal", "cuisine"],
            "electronics": ["phone", "laptop", "computer", "electronics", "tech", "gadget",
                           "headphone", "accessory", "device", "buy tech", "compare products",
                           "smartphone", "tablet"],
            "travel": ["travel", "trip", "flight", "hotel", "vacation", "destination",
                      "book", "flight", "paris", "tokyo", "london", "bali", "new york",
                      "holiday", "journey"]
        }

        for vendor in self.vendors.values():
            vendor_name_lower = vendor.name.lower()

            # Check if any keywords match
            for vendor_type, kw_list in keywords.items():
                if any(kw in vendor_name_lower for kw in [vendor_type]):
                    if any(kw in intent_lower for kw in kw_list):
                        matches.append(vendor)
                        break

            # Also check skill descriptions
            for skill in vendor.skills:
                skill_desc = skill.get("description", "").lower()
                skill_name = skill.get("name", "").lower()
                if intent_lower in skill_desc or intent_lower in skill_name:
                    if vendor not in matches:
                        matches.append(vendor)
                    break

        return matches

    def get_all_healthy_vendors(self) -> list[VendorInfo]:
        """Get all vendors that are currently healthy."""
        return [v for v in self.vendors.values() if v.is_healthy]

    def get_vendor_by_name(self, name: str) -> Optional[VendorInfo]:
        """Find a vendor by name (case-insensitive)."""
        name_lower = name.lower()
        for vendor in self.vendors.values():
            if name_lower in vendor.name.lower():
                return vendor
        return None

    def format_vendors_list(self) -> str:
        """Format the list of vendors for display."""
        if not self.vendors:
            return "No vendors available."

        lines = []
        for i, vendor in enumerate(self.vendors.values(), 1):
            status = "✓" if vendor.is_healthy else "✗"
            lines.append(f"{i}. {vendor.name} [{status}]")
            lines.append(f"   {vendor.description}")
            if vendor.skills:
                skills = ", ".join(s.get("name", s.get("id", "Unknown")) for s in vendor.skills)
                lines.append(f"   Skills: {skills}")

        return "\n".join(lines)


# Singleton registry instance
_registry: Optional[VendorRegistry] = None


async def get_registry() -> VendorRegistry:
    """Get the global vendor registry, initializing if needed."""
    global _registry
    if _registry is None:
        _registry = VendorRegistry()
        await _registry.discover_all()
    return _registry
