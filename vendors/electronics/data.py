"""Mock product data for TechZone Electronics."""

PRODUCTS_DATA = {
    "phones": [
        {
            "id": "phone-001",
            "name": "Galaxy Pro X",
            "description": "Flagship smartphone with 6.7\" AMOLED display, 108MP camera, 5G",
            "price": 999.99,
            "category": "phones",
            "brand": "Samsung",
            "specs": {
                "display": "6.7\" AMOLED",
                "camera": "108MP + 12MP + 10MP",
                "battery": "5000mAh",
                "storage": "256GB",
                "ram": "12GB"
            },
            "in_stock": True,
            "stock_count": 15
        },
        {
            "id": "phone-002",
            "name": "iPhone Ultra",
            "description": "Premium smartphone with A17 chip, ProMotion display, titanium design",
            "price": 1199.99,
            "category": "phones",
            "brand": "Apple",
            "specs": {
                "display": "6.7\" Super Retina XDR",
                "camera": "48MP + 12MP + 12MP",
                "battery": "4500mAh",
                "storage": "256GB",
                "chip": "A17 Pro"
            },
            "in_stock": True,
            "stock_count": 8
        },
        {
            "id": "phone-003",
            "name": "Pixel Prime",
            "description": "AI-powered smartphone with exceptional camera and pure Android",
            "price": 899.99,
            "category": "phones",
            "brand": "Google",
            "specs": {
                "display": "6.7\" LTPO OLED",
                "camera": "50MP + 48MP + 48MP",
                "battery": "5050mAh",
                "storage": "256GB",
                "chip": "Tensor G3"
            },
            "in_stock": True,
            "stock_count": 20
        }
    ],
    "laptops": [
        {
            "id": "laptop-001",
            "name": "MacBook Pro 16",
            "description": "Professional laptop with M3 Max chip, 16\" Liquid Retina XDR display",
            "price": 2499.99,
            "category": "laptops",
            "brand": "Apple",
            "specs": {
                "display": "16\" Liquid Retina XDR",
                "processor": "M3 Max",
                "memory": "36GB",
                "storage": "512GB SSD",
                "battery": "22 hours"
            },
            "in_stock": True,
            "stock_count": 5
        },
        {
            "id": "laptop-002",
            "name": "ThinkPad X1 Carbon",
            "description": "Ultra-light business laptop with Intel Core i7, carbon fiber chassis",
            "price": 1799.99,
            "category": "laptops",
            "brand": "Lenovo",
            "specs": {
                "display": "14\" 2.8K OLED",
                "processor": "Intel Core i7-1365U",
                "memory": "32GB",
                "storage": "1TB SSD",
                "weight": "1.12kg"
            },
            "in_stock": True,
            "stock_count": 12
        },
        {
            "id": "laptop-003",
            "name": "Dell XPS 15",
            "description": "Premium laptop with InfinityEdge display and powerful specs",
            "price": 1999.99,
            "category": "laptops",
            "brand": "Dell",
            "specs": {
                "display": "15.6\" 3.5K OLED",
                "processor": "Intel Core i9-13900H",
                "memory": "32GB",
                "storage": "1TB SSD",
                "graphics": "RTX 4060"
            },
            "in_stock": False,
            "stock_count": 0
        },
        {
            "id": "laptop-004",
            "name": "ROG Zephyrus G14",
            "description": "Compact gaming laptop with AMD Ryzen 9 and RTX 4070",
            "price": 1699.99,
            "category": "laptops",
            "brand": "ASUS",
            "specs": {
                "display": "14\" QHD+ 165Hz",
                "processor": "AMD Ryzen 9 7940HS",
                "memory": "16GB",
                "storage": "1TB SSD",
                "graphics": "RTX 4070"
            },
            "in_stock": True,
            "stock_count": 7
        }
    ],
    "headphones": [
        {
            "id": "head-001",
            "name": "AirPods Max",
            "description": "Premium over-ear headphones with active noise cancellation",
            "price": 549.99,
            "category": "headphones",
            "brand": "Apple",
            "specs": {
                "type": "Over-ear",
                "driver": "40mm",
                "noise_cancellation": "Active",
                "battery": "20 hours",
                "connectivity": "Bluetooth 5.0"
            },
            "in_stock": True,
            "stock_count": 25
        },
        {
            "id": "head-002",
            "name": "Sony WH-1000XM5",
            "description": "Industry-leading noise canceling wireless headphones",
            "price": 399.99,
            "category": "headphones",
            "brand": "Sony",
            "specs": {
                "type": "Over-ear",
                "driver": "30mm",
                "noise_cancellation": "Active",
                "battery": "30 hours",
                "connectivity": "Bluetooth 5.2"
            },
            "in_stock": True,
            "stock_count": 30
        },
        {
            "id": "head-003",
            "name": "Bose QuietComfort Ultra",
            "description": "Premium wireless earbuds with spatial audio",
            "price": 299.99,
            "category": "headphones",
            "brand": "Bose",
            "specs": {
                "type": "In-ear",
                "noise_cancellation": "Active",
                "battery": "6 hours (24 with case)",
                "connectivity": "Bluetooth 5.3",
                "spatial_audio": True
            },
            "in_stock": True,
            "stock_count": 18
        }
    ],
    "accessories": [
        {
            "id": "acc-001",
            "name": "MagSafe Charger",
            "description": "Wireless charger with magnetic alignment for iPhone",
            "price": 39.99,
            "category": "accessories",
            "brand": "Apple",
            "specs": {
                "power": "15W",
                "compatibility": "iPhone 12+, AirPods",
                "cable_length": "1m"
            },
            "in_stock": True,
            "stock_count": 50
        },
        {
            "id": "acc-002",
            "name": "USB-C Hub Pro",
            "description": "7-in-1 USB-C hub with HDMI, USB-A, SD card reader",
            "price": 79.99,
            "category": "accessories",
            "brand": "Anker",
            "specs": {
                "ports": "2x USB-A, 1x USB-C, HDMI, SD, microSD, 3.5mm",
                "hdmi_output": "4K@60Hz",
                "power_delivery": "100W"
            },
            "in_stock": True,
            "stock_count": 35
        },
        {
            "id": "acc-003",
            "name": "Mechanical Keyboard",
            "description": "Wireless mechanical keyboard with hot-swappable switches",
            "price": 149.99,
            "category": "accessories",
            "brand": "Keychron",
            "specs": {
                "switches": "Gateron Brown",
                "layout": "75%",
                "connectivity": "Bluetooth/USB-C",
                "battery": "4000mAh",
                "backlighting": "RGB"
            },
            "in_stock": True,
            "stock_count": 22
        },
        {
            "id": "acc-004",
            "name": "4K Webcam",
            "description": "Professional 4K webcam with auto-framing and noise reduction",
            "price": 199.99,
            "category": "accessories",
            "brand": "Logitech",
            "specs": {
                "resolution": "4K@30fps, 1080p@60fps",
                "field_of_view": "90°",
                "microphones": "Dual omnidirectional",
                "autofocus": True
            },
            "in_stock": True,
            "stock_count": 15
        }
    ]
}


def get_all_products() -> list[dict]:
    """Get all products."""
    products = []
    for category_products in PRODUCTS_DATA.values():
        products.extend(category_products)
    return products


def get_categories() -> list[str]:
    """Get all product categories."""
    return list(PRODUCTS_DATA.keys())


def get_products_by_category(category: str) -> list[dict]:
    """Get products in a specific category."""
    return PRODUCTS_DATA.get(category, [])


def get_product_by_id(product_id: str) -> dict | None:
    """Get a specific product by ID."""
    for products in PRODUCTS_DATA.values():
        for product in products:
            if product["id"] == product_id:
                return product
    return None


def search_products(query: str) -> list[dict]:
    """Search products by name, description, or brand."""
    query = query.lower()
    results = []
    for products in PRODUCTS_DATA.values():
        for product in products:
            if (query in product["name"].lower() or
                query in product["description"].lower() or
                query in product.get("brand", "").lower()):
                results.append(product)
    return results


def compare_products(product_ids: list[str]) -> list[dict]:
    """Get multiple products for comparison."""
    results = []
    for product_id in product_ids:
        product = get_product_by_id(product_id)
        if product:
            results.append(product)
    return results


def check_availability(product_id: str) -> dict:
    """Check availability of a product."""
    product = get_product_by_id(product_id)
    if not product:
        return {"error": f"Product {product_id} not found"}
    return {
        "product_id": product_id,
        "name": product["name"],
        "in_stock": product["in_stock"],
        "stock_count": product["stock_count"],
        "delivery_estimate": "2-3 business days" if product["in_stock"] else "Out of stock"
    }
