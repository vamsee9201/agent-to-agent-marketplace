"""ADK agent for Wanderlust Travel."""

import os
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .tools import TOOLS

# Lazy initialization
_agent_instance = None
_session_service = None

# Ensure Vertex AI environment variables are set
# ADK reads these automatically for Vertex AI configuration
# GOOGLE_CLOUD_PROJECT must be set via .env file or environment
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")

APP_NAME = "wanderlust_travel"


def get_session_service() -> InMemorySessionService:
    """Get or create the session service (lazy initialization)."""
    global _session_service
    if _session_service is None:
        _session_service = InMemorySessionService()
    return _session_service


# System instruction for the travel agent
SYSTEM_INSTRUCTION = """You are a helpful travel consultant for Wanderlust Travel.
You help customers with:
- Discovering travel destinations
- Finding flights to their desired destinations
- Searching for hotels and accommodations
- Getting package deals that combine flights and hotels
- Providing travel quotes and estimates

Be friendly, knowledgeable about travel, and always use the available tools to provide
accurate, up-to-date information. When helping plan a trip:
1. First understand the customer's preferences (destination, dates, budget)
2. Search for relevant destinations if they're undecided
3. Show flight options
4. Recommend suitable hotels
5. Mention package deals if available for better value

Always provide helpful travel tips when appropriate.
"""


def create_travel_agent() -> LlmAgent:
    """Create the ADK travel agent."""
    # ADK uses environment variables for Vertex AI configuration:
    # GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION
    return LlmAgent(
        name="wanderlust_travel",
        model="gemini-2.0-flash-001",
        instruction=SYSTEM_INSTRUCTION,
        tools=TOOLS,
    )


def get_travel_agent() -> LlmAgent:
    """Get or create the travel agent (lazy initialization)."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_travel_agent()
    return _agent_instance


async def process_message(message: str, history: list = None, session_id: str = None) -> str:
    """Process a user message and return the agent's response."""
    import uuid

    # Create a runner for the agent with session service
    agent = get_travel_agent()
    session_service = get_session_service()

    # Generate session ID if not provided
    if session_id is None:
        session_id = str(uuid.uuid4())

    # Create session before creating runner
    user_id = "demo_user"
    existing_session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
    if existing_session is None:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

    # Create runner after session exists
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Run the agent
    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(
            role="user",
            parts=[types.Part(text=message)]
        )
    ):
        if hasattr(event, 'content') and event.content:
            for part in event.content.parts:
                if hasattr(part, 'text') and part.text:
                    response_text += part.text

    return response_text if response_text else "I'm sorry, I couldn't process your request."
