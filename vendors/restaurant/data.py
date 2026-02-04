"""Mock menu data for Bella's Italian Restaurant."""

MENU_DATA = {
    "appetizers": [
        {
            "id": "app-001",
            "name": "Bruschetta",
            "description": "Toasted bread topped with fresh tomatoes, basil, and garlic",
            "price": 8.99,
            "category": "appetizers",
            "dietary": ["vegetarian"]
        },
        {
            "id": "app-002",
            "name": "Calamari Fritti",
            "description": "Crispy fried calamari served with marinara sauce",
            "price": 12.99,
            "category": "appetizers",
            "dietary": []
        },
        {
            "id": "app-003",
            "name": "Caprese Salad",
            "description": "Fresh mozzarella, tomatoes, and basil with balsamic glaze",
            "price": 10.99,
            "category": "appetizers",
            "dietary": ["vegetarian", "gluten-free"]
        }
    ],
    "pizzas": [
        {
            "id": "piz-001",
            "name": "Margherita",
            "description": "Classic pizza with tomato sauce, mozzarella, and fresh basil",
            "price": 14.99,
            "category": "pizzas",
            "dietary": ["vegetarian"]
        },
        {
            "id": "piz-002",
            "name": "Pepperoni",
            "description": "Tomato sauce, mozzarella, and spicy pepperoni",
            "price": 16.99,
            "category": "pizzas",
            "dietary": []
        },
        {
            "id": "piz-003",
            "name": "Quattro Formaggi",
            "description": "Four cheese pizza with mozzarella, gorgonzola, parmesan, and fontina",
            "price": 17.99,
            "category": "pizzas",
            "dietary": ["vegetarian"]
        },
        {
            "id": "piz-004",
            "name": "Diavola",
            "description": "Spicy pizza with nduja, pepperoni, and chili flakes",
            "price": 18.99,
            "category": "pizzas",
            "dietary": []
        }
    ],
    "pastas": [
        {
            "id": "pas-001",
            "name": "Spaghetti Carbonara",
            "description": "Spaghetti with egg, pecorino cheese, guanciale, and black pepper",
            "price": 15.99,
            "category": "pastas",
            "dietary": []
        },
        {
            "id": "pas-002",
            "name": "Fettuccine Alfredo",
            "description": "Fettuccine in a rich, creamy parmesan sauce",
            "price": 14.99,
            "category": "pastas",
            "dietary": ["vegetarian"]
        },
        {
            "id": "pas-003",
            "name": "Penne Arrabbiata",
            "description": "Penne pasta in spicy tomato sauce with garlic and chili",
            "price": 13.99,
            "category": "pastas",
            "dietary": ["vegetarian", "vegan"]
        },
        {
            "id": "pas-004",
            "name": "Lasagna Bolognese",
            "description": "Layers of pasta with beef ragu, bechamel, and parmesan",
            "price": 17.99,
            "category": "pastas",
            "dietary": []
        }
    ],
    "desserts": [
        {
            "id": "des-001",
            "name": "Tiramisu",
            "description": "Classic Italian dessert with espresso-soaked ladyfingers and mascarpone",
            "price": 8.99,
            "category": "desserts",
            "dietary": ["vegetarian"]
        },
        {
            "id": "des-002",
            "name": "Panna Cotta",
            "description": "Creamy vanilla panna cotta with berry compote",
            "price": 7.99,
            "category": "desserts",
            "dietary": ["vegetarian", "gluten-free"]
        },
        {
            "id": "des-003",
            "name": "Cannoli",
            "description": "Crispy pastry shells filled with sweet ricotta cream",
            "price": 6.99,
            "category": "desserts",
            "dietary": ["vegetarian"]
        }
    ]
}


def get_all_items() -> list[dict]:
    """Get all menu items."""
    items = []
    for category_items in MENU_DATA.values():
        items.extend(category_items)
    return items


def get_categories() -> list[str]:
    """Get all menu categories."""
    return list(MENU_DATA.keys())


def get_items_by_category(category: str) -> list[dict]:
    """Get items in a specific category."""
    return MENU_DATA.get(category, [])


def get_item_by_id(item_id: str) -> dict | None:
    """Get a specific menu item by ID."""
    for items in MENU_DATA.values():
        for item in items:
            if item["id"] == item_id:
                return item
    return None


def search_items(query: str) -> list[dict]:
    """Search menu items by name or description."""
    query = query.lower()
    results = []
    for items in MENU_DATA.values():
        for item in items:
            if query in item["name"].lower() or query in item["description"].lower():
                results.append(item)
    return results
