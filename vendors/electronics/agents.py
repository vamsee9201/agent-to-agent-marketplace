"""CrewAI agents for TechZone Electronics."""

import os
from crewai import Agent
from crewai.tools import tool
from langchain_google_vertexai import ChatVertexAI
from .mcp_server import ElectronicsMCPTools

# Vertex AI configuration - set via environment variables
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")


# Define tools using CrewAI's tool decorator
@tool
def get_products(category: str = "") -> str:
    """Get products, optionally filtered by category (phones, laptops, headphones, accessories)."""
    return ElectronicsMCPTools.get_products(category if category else None)


@tool
def get_categories() -> str:
    """Get all available product categories."""
    return ElectronicsMCPTools.get_categories()


@tool
def search_products(query: str) -> str:
    """Search for products by name, description, or brand."""
    return ElectronicsMCPTools.search_products(query)


@tool
def get_product_details(product_id: str) -> str:
    """Get detailed information about a specific product."""
    return ElectronicsMCPTools.get_product_details(product_id)


@tool
def compare_products(product_ids: str) -> str:
    """Compare multiple products. Pass comma-separated product IDs."""
    return ElectronicsMCPTools.compare_products(product_ids)


@tool
def check_availability(product_id: str) -> str:
    """Check stock availability and delivery estimate for a product."""
    return ElectronicsMCPTools.check_availability(product_id)


# List of all tools
TOOLS = [
    get_products,
    get_categories,
    search_products,
    get_product_details,
    compare_products,
    check_availability,
]


def create_electronics_agent() -> Agent:
    """Create the electronics product expert agent."""
    # Use LangChain's ChatVertexAI directly - CrewAI supports LangChain LLMs
    llm = ChatVertexAI(
        model="gemini-2.0-flash-001",
        project=GOOGLE_CLOUD_PROJECT,
        location=GOOGLE_CLOUD_LOCATION,
    )

    return Agent(
        role="Electronics Product Expert",
        goal="Help customers find, compare, and purchase electronics",
        backstory="""You are an expert electronics sales consultant at TechZone Electronics.
        You have deep knowledge of consumer electronics including smartphones, laptops,
        headphones, and accessories. You help customers find the perfect products for their
        needs, compare options, and make informed purchasing decisions.

        You are friendly, helpful, and always provide accurate product information using
        the available tools. When comparing products, you highlight key differences to
        help customers choose. You also check availability before recommending products.""",
        tools=TOOLS,
        verbose=False,
        allow_delegation=False,
        llm=llm,
    )
