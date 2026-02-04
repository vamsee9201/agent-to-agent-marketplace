"""A2A Server entry point for Bella's Italian Restaurant."""

import os
import uvicorn
from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

from .agent_executor import RestaurantAgentExecutor

# Load environment variables
load_dotenv()

# Agent configuration
AGENT_CARD = AgentCard(
    name="Bella's Italian Restaurant",
    description="Italian restaurant with pizza, pasta, appetizers, and desserts. Browse our menu, search for dishes, get recommendations, and place orders.",
    url="http://localhost:10001",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    skills=[
        AgentSkill(
            id="browse_menu",
            name="Browse Menu",
            description="View available dishes and categories",
            tags=["menu", "food"]
        ),
        AgentSkill(
            id="search_dishes",
            name="Search Dishes",
            description="Search for specific dishes by name or ingredient",
            tags=["search", "food"]
        ),
        AgentSkill(
            id="get_recommendations",
            name="Get Recommendations",
            description="Get dish recommendations based on dietary preferences",
            tags=["recommendations", "food"]
        ),
        AgentSkill(
            id="place_order",
            name="Place Order",
            description="Place an order for selected dishes",
            tags=["order", "food"]
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
    executor = RestaurantAgentExecutor()

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
    print("Starting Bella's Italian Restaurant A2A Server on port 10001...")
    print("Agent Card available at: http://localhost:10001/.well-known/agent.json")
    uvicorn.run(app, host="0.0.0.0", port=10001)


if __name__ == "__main__":
    main()
