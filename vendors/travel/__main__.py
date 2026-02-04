"""A2A Server entry point for Wanderlust Travel."""

import os
import uvicorn
from dotenv import load_dotenv
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCard, AgentSkill, AgentCapabilities

from .agent_executor import TravelAgentExecutor

# Load environment variables
load_dotenv()

# Ensure GOOGLE_CLOUD_LOCATION has a default if not set
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")

# Agent configuration
AGENT_CARD = AgentCard(
    name="Wanderlust Travel",
    description="Travel booking service for flights, hotels, and vacation packages. Search destinations, find flights, book hotels, and get package deals.",
    url="http://localhost:10003",
    version="1.0.0",
    defaultInputModes=["text"],
    defaultOutputModes=["text"],
    skills=[
        AgentSkill(
            id="search_destinations",
            name="Search Destinations",
            description="Find travel destinations and get information about them",
            tags=["search", "travel"]
        ),
        AgentSkill(
            id="search_flights",
            name="Search Flights",
            description="Search available flights to destinations",
            tags=["flights", "travel"]
        ),
        AgentSkill(
            id="search_hotels",
            name="Search Hotels",
            description="Search hotels at destinations",
            tags=["hotels", "travel"]
        ),
        AgentSkill(
            id="book_package",
            name="Book Package",
            description="Book a complete travel package with flights and hotel",
            tags=["booking", "travel"]
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
    executor = TravelAgentExecutor()

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
    print("Starting Wanderlust Travel A2A Server on port 10003...")
    print("Agent Card available at: http://localhost:10003/.well-known/agent.json")
    uvicorn.run(app, host="0.0.0.0", port=10003)


if __name__ == "__main__":
    main()
