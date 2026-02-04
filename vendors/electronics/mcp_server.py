"""MCP Server for Electronics product data."""

import json
from . import data


class ElectronicsMCPTools:
    """MCP-style tools for accessing electronics product data."""

    @staticmethod
    def get_products(category: str = None) -> str:
        """Get products, optionally filtered by category.

        Args:
            category: Optional category filter (phones, laptops, headphones, accessories)
        """
        if category:
            products = data.get_products_by_category(category)
            if not products:
                return json.dumps({"error": f"Category '{category}' not found"})
            return json.dumps({"category": category, "products": products})
        else:
            # Return summary of all categories
            summary = {}
            for cat in data.get_categories():
                products = data.get_products_by_category(cat)
                summary[cat] = [
                    {
                        "id": p["id"],
                        "name": p["name"],
                        "price": f"${p['price']:.2f}",
                        "brand": p["brand"]
                    }
                    for p in products
                ]
            return json.dumps(summary, indent=2)

    @staticmethod
    def get_categories() -> str:
        """Get all available product categories."""
        return json.dumps({"categories": data.get_categories()})

    @staticmethod
    def search_products(query: str) -> str:
        """Search for products by name, description, or brand.

        Args:
            query: Search term
        """
        results = data.search_products(query)
        return json.dumps({
            "query": query,
            "results": results,
            "count": len(results)
        })

    @staticmethod
    def get_product_details(product_id: str) -> str:
        """Get detailed information about a specific product.

        Args:
            product_id: The unique identifier for the product
        """
        product = data.get_product_by_id(product_id)
        if not product:
            return json.dumps({"error": f"Product with ID '{product_id}' not found"})
        return json.dumps(product, indent=2)

    @staticmethod
    def compare_products(product_ids: str) -> str:
        """Compare multiple products side by side.

        Args:
            product_ids: Comma-separated list of product IDs to compare
        """
        ids = [pid.strip() for pid in product_ids.split(",")]
        products = data.compare_products(ids)

        if not products:
            return json.dumps({"error": "No valid products found for comparison"})

        comparison = {
            "products": products,
            "comparison_table": {}
        }

        # Build comparison table for common attributes
        if products:
            comparison["comparison_table"] = {
                "names": [p["name"] for p in products],
                "prices": [f"${p['price']:.2f}" for p in products],
                "brands": [p.get("brand", "N/A") for p in products],
                "availability": [
                    "In Stock" if p.get("in_stock") else "Out of Stock"
                    for p in products
                ]
            }

        return json.dumps(comparison, indent=2)

    @staticmethod
    def check_availability(product_id: str) -> str:
        """Check stock availability and delivery estimate.

        Args:
            product_id: The unique identifier for the product
        """
        availability = data.check_availability(product_id)
        return json.dumps(availability, indent=2)
