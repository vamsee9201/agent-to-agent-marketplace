"""MCP Server for Travel data."""

import json
from . import data


class TravelMCPTools:
    """MCP-style tools for accessing travel data."""

    @staticmethod
    def get_destinations() -> str:
        """Get all available travel destinations."""
        destinations = data.get_all_destinations()
        return json.dumps({
            "destinations": [
                {
                    "id": d["id"],
                    "name": d["name"],
                    "country": d["country"],
                    "description": d["description"]
                }
                for d in destinations
            ]
        }, indent=2)

    @staticmethod
    def get_destination_details(destination: str) -> str:
        """Get detailed information about a specific destination.

        Args:
            destination: Destination name or ID
        """
        dest = data.get_destination(destination)
        if not dest:
            return json.dumps({"error": f"Destination '{destination}' not found"})
        return json.dumps(dest, indent=2)

    @staticmethod
    def search_destinations(query: str) -> str:
        """Search for destinations by name, country, or description.

        Args:
            query: Search term
        """
        results = data.search_destinations(query)
        return json.dumps({
            "query": query,
            "results": results,
            "count": len(results)
        }, indent=2)

    @staticmethod
    def search_flights(destination: str, from_city: str = "") -> str:
        """Search for flights to a destination.

        Args:
            destination: Destination city name
            from_city: Optional departure city filter
        """
        flights = data.get_flights(destination)

        if from_city:
            from_city_lower = from_city.lower()
            flights = [f for f in flights if from_city_lower in f["departure_city"].lower()]

        if not flights:
            return json.dumps({
                "error": f"No flights found to '{destination}'" +
                        (f" from '{from_city}'" if from_city else "")
            })

        return json.dumps({
            "destination": destination,
            "from_city": from_city if from_city else "All cities",
            "flights": flights,
            "count": len(flights)
        }, indent=2)

    @staticmethod
    def search_hotels(destination: str, min_rating: int = 0) -> str:
        """Search for hotels at a destination.

        Args:
            destination: Destination city name
            min_rating: Optional minimum star rating filter (1-5)
        """
        hotels = data.get_hotels(destination)

        if min_rating > 0:
            hotels = [h for h in hotels if h["rating"] >= min_rating]

        if not hotels:
            return json.dumps({
                "error": f"No hotels found in '{destination}'" +
                        (f" with {min_rating}+ stars" if min_rating else "")
            })

        return json.dumps({
            "destination": destination,
            "min_rating": min_rating if min_rating else "Any",
            "hotels": hotels,
            "count": len(hotels)
        }, indent=2)

    @staticmethod
    def get_package_deals(destination: str = "") -> str:
        """Get package deals, optionally for a specific destination.

        Args:
            destination: Optional destination to filter packages
        """
        if destination:
            package = data.get_package(destination)
            if not package:
                return json.dumps({"error": f"No package found for '{destination}'"})
            return json.dumps(package, indent=2)
        else:
            # Return all packages
            packages = []
            for dest_key in data.PACKAGES:
                packages.append(data.PACKAGES[dest_key])
            return json.dumps({"packages": packages}, indent=2)

    @staticmethod
    def get_travel_quote(destination: str, nights: int = 5) -> str:
        """Get a travel quote for a destination.

        Args:
            destination: Destination name
            nights: Number of nights (default 5)
        """
        flights = data.get_flights(destination)
        hotels = data.get_hotels(destination)

        if not flights or not hotels:
            return json.dumps({"error": f"Unable to create quote for '{destination}'"})

        # Get cheapest options
        cheapest_flight = min(flights, key=lambda x: x["price"])
        cheapest_hotel = min(hotels, key=lambda x: x["price_per_night"])

        total_flight = cheapest_flight["price"] * 2  # Round trip
        total_hotel = cheapest_hotel["price_per_night"] * nights
        total = total_flight + total_hotel

        return json.dumps({
            "destination": destination,
            "nights": nights,
            "flight": {
                "details": f"{cheapest_flight['airline']} - {cheapest_flight['departure_city']} to {cheapest_flight['arrival_city']}",
                "price": f"${cheapest_flight['price']:.2f} (each way)",
                "total": f"${total_flight:.2f}"
            },
            "hotel": {
                "name": cheapest_hotel["name"],
                "rating": f"{cheapest_hotel['rating']} stars",
                "price_per_night": f"${cheapest_hotel['price_per_night']:.2f}",
                "total": f"${total_hotel:.2f}"
            },
            "estimated_total": f"${total:.2f}",
            "note": "This is an estimate. Package deals may offer better value."
        }, indent=2)
