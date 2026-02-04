"""MCP Server for Restaurant menu data."""

import json
from . import data


class RestaurantMCPTools:
    """MCP-style tools for accessing restaurant menu data."""

    @staticmethod
    def get_menu() -> str:
        """Get the complete restaurant menu organized by category."""
        menu = {}
        for category in data.get_categories():
            items = data.get_items_by_category(category)
            menu[category] = [
                {
                    "id": item["id"],
                    "name": item["name"],
                    "description": item["description"],
                    "price": f"${item['price']:.2f}"
                }
                for item in items
            ]
        return json.dumps(menu, indent=2)

    @staticmethod
    def get_categories() -> str:
        """Get all available menu categories."""
        categories = data.get_categories()
        return json.dumps({"categories": categories})

    @staticmethod
    def get_items_by_category(category: str) -> str:
        """Get all items in a specific category.

        Args:
            category: The category name (appetizers, pizzas, pastas, desserts)
        """
        items = data.get_items_by_category(category)
        if not items:
            return json.dumps({"error": f"Category '{category}' not found"})
        return json.dumps({"category": category, "items": items})

    @staticmethod
    def search_dishes(query: str) -> str:
        """Search for dishes by name or description.

        Args:
            query: Search term to find in dish names or descriptions
        """
        results = data.search_items(query)
        return json.dumps({"query": query, "results": results, "count": len(results)})

    @staticmethod
    def get_dish_details(dish_id: str) -> str:
        """Get detailed information about a specific dish.

        Args:
            dish_id: The unique identifier for the dish
        """
        item = data.get_item_by_id(dish_id)
        if not item:
            return json.dumps({"error": f"Dish with ID '{dish_id}' not found"})
        return json.dumps(item)

    @staticmethod
    def get_recommendations(preference: str = None) -> str:
        """Get dish recommendations based on preferences.

        Args:
            preference: Optional dietary preference (vegetarian, vegan, gluten-free)
        """
        all_items = data.get_all_items()

        if preference:
            preference = preference.lower()
            recommendations = [
                item for item in all_items
                if preference in [d.lower() for d in item.get("dietary", [])]
            ]
        else:
            # Return popular items (one from each category)
            recommendations = []
            for category in data.get_categories():
                items = data.get_items_by_category(category)
                if items:
                    recommendations.append(items[0])

        return json.dumps({
            "preference": preference,
            "recommendations": recommendations
        })
