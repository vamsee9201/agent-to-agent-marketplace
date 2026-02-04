"""A2A Server entry point for TechZone Electronics."""

import os
import uvicorn
from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

from .a2a_server import ElectronicsAgentExecutor

# Load environment variables
load_dotenv()

# Ensure GOOGLE_CLOUD_LOCATION has a default if not set
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")

# Agent configuration
AGENT_CARD = AgentCard(
    name="TechZone Electronics",
    description="Consumer electronics store with phones, laptops, headphones, and accessories. Browse products, compare specs, check availability, and make purchases.",
    url="http://localhost:10002",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    skills=[
        AgentSkill(
            id="browse_products",
            name="Browse Products",
            description="View available electronics by category",
            tags=["browse", "electronics"]
        ),
        AgentSkill(
            id="compare_products",
            name="Compare Products",
            description="Compare specifications of multiple products",
            tags=["compare", "electronics"]
        ),
        AgentSkill(
            id="check_availability",
            name="Check Availability",
            description="Check stock and delivery options",
            tags=["availability", "electronics"]
        ),
        AgentSkill(
            id="place_order",
            name="Place Order",
            description="Purchase selected products",
            tags=["order", "electronics"]
        )
    ],
    capabilities=AgentCapabilities(
        streaming=False,
        pushNotifications=False
    )
)


def create_app():
    """Create the A2A Starlette application."""

    # Create the agent executor
    executor = ElectronicsAgentExecutor()

    # Create the request handler with in-memory task store
    task_store = InMemoryTaskStore()
    handler = DefaultRequestHandler(
        agent_executor=executor,
        task_store=task_store
    )

    # Create the A2A application
    app = A2AStarletteApplication(
        agent_card=AGENT_CARD,
        http_handler=handler
    )

    return app.build()


def main():
    """Run the A2A server."""
    app = create_app()
    print("Starting TechZone Electronics A2A Server on port 10002...")
    print("Agent Card available at: http://localhost:10002/.well-known/agent.json")
    uvicorn.run(app, host="0.0.0.0", port=10002)


if __name__ == "__main__":
    main()
