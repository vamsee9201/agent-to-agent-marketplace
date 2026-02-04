"""LangChain tools wrapping MCP server functionality."""

from langchain_core.tools import tool
from .mcp_server import RestaurantMCPTools


@tool
def get_menu() -> str:
    """Get the complete restaurant menu organized by category."""
    return RestaurantMCPTools.get_menu()


@tool
def get_categories() -> str:
    """Get all available menu categories."""
    return RestaurantMCPTools.get_categories()


@tool
def get_items_by_category(category: str) -> str:
    """Get all items in a specific category.

    Args:
        category: The category name (appetizers, pizzas, pastas, desserts)
    """
    return RestaurantMCPTools.get_items_by_category(category)


@tool
def search_dishes(query: str) -> str:
    """Search for dishes by name or description.

    Args:
        query: Search term to find in dish names or descriptions
    """
    return RestaurantMCPTools.search_dishes(query)


@tool
def get_dish_details(dish_id: str) -> str:
    """Get detailed information about a specific dish.

    Args:
        dish_id: The unique identifier for the dish
    """
    return RestaurantMCPTools.get_dish_details(dish_id)


@tool
def get_recommendations(preference: str = "") -> str:
    """Get dish recommendations based on dietary preferences.

    Args:
        preference: Optional dietary preference (vegetarian, vegan, gluten-free)
    """
    return RestaurantMCPTools.get_recommendations(preference if preference else None)


# List of all tools for the agent
TOOLS = [
    get_menu,
    get_categories,
    get_items_by_category,
    search_dishes,
    get_dish_details,
    get_recommendations,
]
