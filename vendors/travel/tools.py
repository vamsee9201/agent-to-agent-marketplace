"""ADK tools for travel data access."""

from google.adk.tools import FunctionTool
from .mcp_server import TravelMCPTools


def get_destinations() -> str:
    """Get all available travel destinations."""
    return TravelMCPTools.get_destinations()


def get_destination_details(destination: str) -> str:
    """Get detailed information about a specific destination.

    Args:
        destination: Destination name or ID
    """
    return TravelMCPTools.get_destination_details(destination)


def search_destinations(query: str) -> str:
    """Search for destinations by name, country, or description.

    Args:
        query: Search term
    """
    return TravelMCPTools.search_destinations(query)


def search_flights(destination: str, from_city: str = "") -> str:
    """Search for flights to a destination.

    Args:
        destination: Destination city name
        from_city: Optional departure city filter
    """
    return TravelMCPTools.search_flights(destination, from_city)


def search_hotels(destination: str, min_rating: int = 0) -> str:
    """Search for hotels at a destination.

    Args:
        destination: Destination city name
        min_rating: Optional minimum star rating filter (1-5)
    """
    return TravelMCPTools.search_hotels(destination, min_rating)


def get_package_deals(destination: str = "") -> str:
    """Get package deals, optionally for a specific destination.

    Args:
        destination: Optional destination to filter packages
    """
    return TravelMCPTools.get_package_deals(destination)


def get_travel_quote(destination: str, nights: int = 5) -> str:
    """Get a travel quote for a destination with estimated costs.

    Args:
        destination: Destination name
        nights: Number of nights (default 5)
    """
    return TravelMCPTools.get_travel_quote(destination, nights)


# List of all tools for the agent
TOOLS = [
    get_destinations,
    get_destination_details,
    search_destinations,
    search_flights,
    search_hotels,
    get_package_deals,
    get_travel_quote,
]
