"""Mock travel data for Wanderlust Travel."""

from datetime import datetime, timedelta

# Generate some dates for mock data
today = datetime.now()
next_week = today + timedelta(days=7)
next_month = today + timedelta(days=30)


DESTINATIONS = {
    "paris": {
        "id": "dest-001",
        "name": "Paris",
        "country": "France",
        "description": "The City of Light - home to the Eiffel Tower, Louvre, and world-class cuisine",
        "highlights": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Champs-Élysées"],
        "best_season": "Spring (April-June)",
        "currency": "EUR"
    },
    "tokyo": {
        "id": "dest-002",
        "name": "Tokyo",
        "country": "Japan",
        "description": "A perfect blend of ancient traditions and cutting-edge technology",
        "highlights": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Tower", "Tsukiji Market"],
        "best_season": "Spring (March-May) or Fall (September-November)",
        "currency": "JPY"
    },
    "new_york": {
        "id": "dest-003",
        "name": "New York",
        "country": "USA",
        "description": "The city that never sleeps - iconic skyline, Broadway, and diverse culture",
        "highlights": ["Statue of Liberty", "Central Park", "Times Square", "Empire State Building"],
        "best_season": "Fall (September-November)",
        "currency": "USD"
    },
    "london": {
        "id": "dest-004",
        "name": "London",
        "country": "United Kingdom",
        "description": "Historic capital with royal palaces, world-class museums, and vibrant culture",
        "highlights": ["Big Ben", "Tower of London", "British Museum", "Buckingham Palace"],
        "best_season": "Summer (June-August)",
        "currency": "GBP"
    },
    "bali": {
        "id": "dest-005",
        "name": "Bali",
        "country": "Indonesia",
        "description": "Tropical paradise with beautiful beaches, temples, and rich spiritual culture",
        "highlights": ["Ubud Rice Terraces", "Tanah Lot Temple", "Seminyak Beach", "Mount Batur"],
        "best_season": "Dry Season (April-October)",
        "currency": "IDR"
    }
}

FLIGHTS = {
    "paris": [
        {
            "id": "fl-par-001",
            "airline": "Air France",
            "departure_city": "New York (JFK)",
            "arrival_city": "Paris (CDG)",
            "departure_time": "22:00",
            "arrival_time": "11:30+1",
            "duration": "7h 30m",
            "price": 899.00,
            "class": "Economy",
            "stops": 0
        },
        {
            "id": "fl-par-002",
            "airline": "Delta",
            "departure_city": "Los Angeles (LAX)",
            "arrival_city": "Paris (CDG)",
            "departure_time": "16:30",
            "arrival_time": "12:45+1",
            "duration": "10h 15m",
            "price": 1099.00,
            "class": "Economy",
            "stops": 0
        },
        {
            "id": "fl-par-003",
            "airline": "Air France",
            "departure_city": "New York (JFK)",
            "arrival_city": "Paris (CDG)",
            "departure_time": "19:00",
            "arrival_time": "08:30+1",
            "duration": "7h 30m",
            "price": 2499.00,
            "class": "Business",
            "stops": 0
        }
    ],
    "tokyo": [
        {
            "id": "fl-tok-001",
            "airline": "Japan Airlines",
            "departure_city": "Los Angeles (LAX)",
            "arrival_city": "Tokyo (NRT)",
            "departure_time": "11:30",
            "arrival_time": "15:30+1",
            "duration": "12h 00m",
            "price": 1299.00,
            "class": "Economy",
            "stops": 0
        },
        {
            "id": "fl-tok-002",
            "airline": "ANA",
            "departure_city": "San Francisco (SFO)",
            "arrival_city": "Tokyo (HND)",
            "departure_time": "13:00",
            "arrival_time": "16:30+1",
            "duration": "11h 30m",
            "price": 1199.00,
            "class": "Economy",
            "stops": 0
        }
    ],
    "new_york": [
        {
            "id": "fl-nyc-001",
            "airline": "United",
            "departure_city": "Los Angeles (LAX)",
            "arrival_city": "New York (JFK)",
            "departure_time": "08:00",
            "arrival_time": "16:30",
            "duration": "5h 30m",
            "price": 349.00,
            "class": "Economy",
            "stops": 0
        },
        {
            "id": "fl-nyc-002",
            "airline": "JetBlue",
            "departure_city": "Boston (BOS)",
            "arrival_city": "New York (JFK)",
            "departure_time": "07:00",
            "arrival_time": "08:15",
            "duration": "1h 15m",
            "price": 149.00,
            "class": "Economy",
            "stops": 0
        }
    ],
    "london": [
        {
            "id": "fl-lon-001",
            "airline": "British Airways",
            "departure_city": "New York (JFK)",
            "arrival_city": "London (LHR)",
            "departure_time": "22:00",
            "arrival_time": "10:00+1",
            "duration": "7h 00m",
            "price": 799.00,
            "class": "Economy",
            "stops": 0
        },
        {
            "id": "fl-lon-002",
            "airline": "Virgin Atlantic",
            "departure_city": "Los Angeles (LAX)",
            "arrival_city": "London (LHR)",
            "departure_time": "21:30",
            "arrival_time": "16:00+1",
            "duration": "10h 30m",
            "price": 999.00,
            "class": "Economy",
            "stops": 0
        }
    ],
    "bali": [
        {
            "id": "fl-bal-001",
            "airline": "Singapore Airlines",
            "departure_city": "Los Angeles (LAX)",
            "arrival_city": "Bali (DPS)",
            "departure_time": "23:30",
            "arrival_time": "14:00+2",
            "duration": "20h 30m",
            "price": 1499.00,
            "class": "Economy",
            "stops": 1
        },
        {
            "id": "fl-bal-002",
            "airline": "Qatar Airways",
            "departure_city": "New York (JFK)",
            "arrival_city": "Bali (DPS)",
            "departure_time": "20:00",
            "arrival_time": "11:30+2",
            "duration": "24h 30m",
            "price": 1799.00,
            "class": "Economy",
            "stops": 1
        }
    ]
}

HOTELS = {
    "paris": [
        {
            "id": "htl-par-001",
            "name": "Le Petit Paris Hotel",
            "rating": 4,
            "location": "Marais District",
            "description": "Charming boutique hotel in the heart of historic Paris",
            "amenities": ["Free WiFi", "Breakfast", "Concierge", "Rooftop Bar"],
            "price_per_night": 199.00
        },
        {
            "id": "htl-par-002",
            "name": "Grand Hotel Champs-Élysées",
            "rating": 5,
            "location": "Champs-Élysées",
            "description": "Luxury hotel with Eiffel Tower views",
            "amenities": ["Free WiFi", "Spa", "Fine Dining", "Concierge", "Gym"],
            "price_per_night": 499.00
        },
        {
            "id": "htl-par-003",
            "name": "Montmartre Inn",
            "rating": 3,
            "location": "Montmartre",
            "description": "Cozy hotel near Sacré-Cœur",
            "amenities": ["Free WiFi", "Breakfast"],
            "price_per_night": 129.00
        }
    ],
    "tokyo": [
        {
            "id": "htl-tok-001",
            "name": "Shibuya Crossing Hotel",
            "rating": 4,
            "location": "Shibuya",
            "description": "Modern hotel overlooking the famous crossing",
            "amenities": ["Free WiFi", "Restaurant", "Gym", "Laundry"],
            "price_per_night": 179.00
        },
        {
            "id": "htl-tok-002",
            "name": "Imperial Tokyo",
            "rating": 5,
            "location": "Chiyoda",
            "description": "Historic luxury hotel near the Imperial Palace",
            "amenities": ["Free WiFi", "Spa", "Multiple Restaurants", "Concierge", "Pool"],
            "price_per_night": 549.00
        }
    ],
    "new_york": [
        {
            "id": "htl-nyc-001",
            "name": "Manhattan Midtown Hotel",
            "rating": 4,
            "location": "Midtown",
            "description": "Convenient location near Times Square and Broadway",
            "amenities": ["Free WiFi", "Restaurant", "Gym", "Business Center"],
            "price_per_night": 249.00
        },
        {
            "id": "htl-nyc-002",
            "name": "The Plaza",
            "rating": 5,
            "location": "Central Park South",
            "description": "Iconic luxury hotel overlooking Central Park",
            "amenities": ["Free WiFi", "Spa", "Fine Dining", "Butler Service", "Gym"],
            "price_per_night": 799.00
        }
    ],
    "london": [
        {
            "id": "htl-lon-001",
            "name": "Westminster Lodge",
            "rating": 4,
            "location": "Westminster",
            "description": "Classic British hotel near Big Ben and Parliament",
            "amenities": ["Free WiFi", "Restaurant", "Tea Room", "Concierge"],
            "price_per_night": 219.00
        },
        {
            "id": "htl-lon-002",
            "name": "The Ritz London",
            "rating": 5,
            "location": "Piccadilly",
            "description": "Legendary luxury hotel with exceptional service",
            "amenities": ["Free WiFi", "Spa", "Fine Dining", "Afternoon Tea", "Gym"],
            "price_per_night": 699.00
        }
    ],
    "bali": [
        {
            "id": "htl-bal-001",
            "name": "Ubud Jungle Resort",
            "rating": 4,
            "location": "Ubud",
            "description": "Peaceful retreat surrounded by rice terraces",
            "amenities": ["Free WiFi", "Pool", "Spa", "Yoga Classes", "Restaurant"],
            "price_per_night": 159.00
        },
        {
            "id": "htl-bal-002",
            "name": "Seminyak Beach Villa",
            "rating": 5,
            "location": "Seminyak",
            "description": "Beachfront luxury villas with private pools",
            "amenities": ["Free WiFi", "Private Pool", "Beach Access", "Spa", "Butler"],
            "price_per_night": 399.00
        }
    ]
}

PACKAGES = {
    "paris": {
        "id": "pkg-par-001",
        "name": "Paris Romance Package",
        "description": "5-night romantic getaway including flights, hotel, and Seine cruise",
        "includes": ["Round-trip flights", "5 nights 4-star hotel", "Seine River Cruise", "Eiffel Tower tickets"],
        "price": 2499.00,
        "duration": "6 days / 5 nights"
    },
    "tokyo": {
        "id": "pkg-tok-001",
        "name": "Tokyo Explorer Package",
        "description": "7-night adventure through Tokyo including traditional experiences",
        "includes": ["Round-trip flights", "7 nights hotel", "JR Pass", "Tea Ceremony", "Sushi Making Class"],
        "price": 3299.00,
        "duration": "8 days / 7 nights"
    },
    "bali": {
        "id": "pkg-bal-001",
        "name": "Bali Wellness Retreat",
        "description": "10-night wellness retreat with spa, yoga, and cultural experiences",
        "includes": ["Round-trip flights", "10 nights villa", "Daily Spa", "Yoga Sessions", "Temple Tours"],
        "price": 3999.00,
        "duration": "11 days / 10 nights"
    }
}


def get_all_destinations() -> list[dict]:
    """Get all available destinations."""
    return list(DESTINATIONS.values())


def get_destination(destination_id: str) -> dict | None:
    """Get a specific destination by ID or name."""
    # Try by ID first
    for dest in DESTINATIONS.values():
        if dest["id"] == destination_id:
            return dest
    # Try by name (lowercase key)
    return DESTINATIONS.get(destination_id.lower())


def search_destinations(query: str) -> list[dict]:
    """Search destinations by name, country, or description."""
    query = query.lower()
    results = []
    for dest in DESTINATIONS.values():
        if (query in dest["name"].lower() or
            query in dest["country"].lower() or
            query in dest["description"].lower()):
            results.append(dest)
    return results


def get_flights(destination: str) -> list[dict]:
    """Get available flights to a destination."""
    destination = destination.lower().replace(" ", "_")
    return FLIGHTS.get(destination, [])


def get_hotels(destination: str) -> list[dict]:
    """Get available hotels at a destination."""
    destination = destination.lower().replace(" ", "_")
    return HOTELS.get(destination, [])


def get_package(destination: str) -> dict | None:
    """Get package deal for a destination."""
    destination = destination.lower().replace(" ", "_")
    return PACKAGES.get(destination)


def search_flights(from_city: str, to_city: str) -> list[dict]:
    """Search flights between cities."""
    to_city = to_city.lower().replace(" ", "_")
    flights = FLIGHTS.get(to_city, [])

    # Filter by departure city if specified
    if from_city:
        from_city = from_city.lower()
        flights = [f for f in flights if from_city in f["departure_city"].lower()]

    return flights
