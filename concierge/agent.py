"""Purchasing Concierge Agent - ADK orchestration agent."""

import os
import uuid
import asyncio
import json
import time
from typing import Optional, Callable, Any

import httpx
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv

from .config import REQUEST_TIMEOUT
from .events import EventType, UIEvent, EventCallback, create_event

# Vertex AI configuration - set environment variables for ADK
# GOOGLE_CLOUD_PROJECT must be set via .env file or environment
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
from .discovery import get_registry, VendorRegistry
from .cart import get_cart, CartManager

load_dotenv()

# Global event callback for UI integration
_event_callback: Optional[EventCallback] = None


def set_event_callback(callback: Optional[EventCallback]) -> None:
    """Set the global event callback for UI integration."""
    global _event_callback
    _event_callback = callback


def get_event_callback() -> Optional[EventCallback]:
    """Get the current event callback."""
    return _event_callback


def emit_event(event: UIEvent) -> None:
    """Emit an event to the registered callback if available."""
    callback = get_event_callback()
    if callback is not None:
        try:
            callback(event)
        except Exception as e:
            print(f"Error in event callback: {e}")


# A2A client for communicating with vendor agents
class A2AClient:
    """Simple A2A client for sending messages to vendor agents."""

    def __init__(self, timeout: int = REQUEST_TIMEOUT):
        self.timeout = timeout

    async def send_message(
        self,
        vendor_url: str,
        message: str,
        context_id: str = None,
        vendor_name: str = None
    ) -> dict:
        """Send a message to a vendor agent via A2A protocol."""
        context_id = context_id or str(uuid.uuid4())
        start_time = time.time()

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Create A2A message
            message_id = str(uuid.uuid4())
            payload = {
                "jsonrpc": "2.0",
                "method": "message/send",
                "params": {
                    "message": {
                        "messageId": message_id,
                        "role": "user",
                        "parts": [{"type": "text", "text": message}]
                    },
                    "configuration": {
                        "acceptedOutputModes": ["text"]
                    }
                },
                "id": message_id
            }

            # Emit A2A request event
            emit_event(create_event(
                EventType.A2A_REQUEST,
                vendor_name=vendor_name,
                raw_json=json.dumps(payload, indent=2),
                message=message,
                url=vendor_url,
            ))

            try:
                response = await client.post(
                    vendor_url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )

                duration_ms = (time.time() - start_time) * 1000

                if response.status_code == 200:
                    result = response.json()

                    # Emit A2A response event
                    emit_event(create_event(
                        EventType.A2A_RESPONSE,
                        vendor_name=vendor_name,
                        duration_ms=duration_ms,
                        raw_json=json.dumps(result, indent=2),
                        status_code=response.status_code,
                    ))

                    return self._extract_response(result)
                else:
                    # Emit error response event
                    emit_event(create_event(
                        EventType.A2A_RESPONSE,
                        vendor_name=vendor_name,
                        duration_ms=duration_ms,
                        raw_json=json.dumps({"error": f"Status {response.status_code}"}, indent=2),
                        status_code=response.status_code,
                    ))
                    return {"error": f"Request failed with status {response.status_code}"}

            except Exception as e:
                duration_ms = (time.time() - start_time) * 1000
                # Emit error event
                emit_event(create_event(
                    EventType.ERROR,
                    vendor_name=vendor_name,
                    duration_ms=duration_ms,
                    message=str(e),
                ))
                return {"error": str(e)}

    def _extract_response(self, result: dict) -> dict:
        """Extract the response text from A2A result."""
        try:
            if "result" in result:
                task_result = result["result"]

                # Handle status updates
                if "status" in task_result:
                    status = task_result["status"]
                    if "message" in status:
                        message = status["message"]
                        if "parts" in message:
                            texts = []
                            for part in message["parts"]:
                                if isinstance(part, dict) and "text" in part:
                                    texts.append(part["text"])
                            return {"response": " ".join(texts)}

                # Handle artifacts
                if "artifacts" in task_result:
                    for artifact in task_result["artifacts"]:
                        if "parts" in artifact:
                            texts = []
                            for part in artifact["parts"]:
                                if isinstance(part, dict) and "text" in part:
                                    texts.append(part["text"])
                            return {"response": " ".join(texts)}

            return {"error": "Could not parse response", "raw": result}
        except Exception as e:
            return {"error": str(e), "raw": result}


# Initialize the A2A client
a2a_client = A2AClient()


# Tool functions for the concierge agent
async def discover_vendors() -> str:
    """Discover and list all available vendor agents."""
    registry = await get_registry()
    await registry.health_check()
    return registry.format_vendors_list()


async def query_vendor(vendor_name: str, message: str) -> str:
    """Send a query to a specific vendor agent.

    Args:
        vendor_name: The name of the vendor to query (e.g., "restaurant", "electronics", "travel")
        message: The message to send to the vendor
    """
    # Emit tool call start event
    emit_event(create_event(
        EventType.TOOL_CALL_START,
        message=f"query_vendor({vendor_name})",
        tool_name="query_vendor",
        vendor_name=vendor_name,
    ))

    registry = await get_registry()
    vendor = registry.get_vendor_by_name(vendor_name)

    if not vendor:
        available = ", ".join(v.name for v in registry.vendors.values())
        emit_event(create_event(
            EventType.TOOL_CALL_END,
            message=f"Vendor '{vendor_name}' not found",
            tool_name="query_vendor",
        ))
        return f"Vendor '{vendor_name}' not found. Available vendors: {available}"

    if not vendor.is_healthy:
        emit_event(create_event(
            EventType.TOOL_CALL_END,
            message=f"Vendor '{vendor.name}' unavailable",
            tool_name="query_vendor",
            vendor_name=vendor.name,
        ))
        return f"Vendor '{vendor.name}' is currently unavailable. Please try again later."

    # Emit vendor query start
    emit_event(create_event(
        EventType.VENDOR_QUERY_START,
        vendor_name=vendor.name,
        message=message,
    ))

    result = await a2a_client.send_message(vendor.url, message, vendor_name=vendor.name)

    # Emit vendor query end
    emit_event(create_event(
        EventType.VENDOR_QUERY_END,
        vendor_name=vendor.name,
    ))

    if "error" in result:
        return f"Error communicating with {vendor.name}: {result['error']}"

    return f"Response from {vendor.name}:\n{result.get('response', 'No response received')}"


async def add_to_cart(
    item_name: str,
    price: float,
    vendor_name: str,
    quantity: int = 1,
    description: str = ""
) -> str:
    """Add an item to the shopping cart.

    Args:
        item_name: Name of the item to add
        price: Price of the item
        vendor_name: Name of the vendor (e.g., "Bella's Italian Restaurant")
        quantity: Number of items to add (default 1)
        description: Optional description of the item
    """
    registry = await get_registry()
    vendor = registry.get_vendor_by_name(vendor_name)

    if not vendor:
        return f"Vendor '{vendor_name}' not found."

    cart = get_cart()
    item = cart.add_item(
        name=item_name,
        price=price,
        vendor_id=vendor.url,
        vendor_name=vendor.name,
        quantity=quantity,
        description=description
    )

    return f"Added to cart: {item_name} x{quantity} @ ${price:.2f} from {vendor.name}"


def view_cart() -> str:
    """View the current shopping cart."""
    cart = get_cart()
    return cart.format_cart()


def checkout() -> str:
    """Complete the purchase and create orders for all items in the cart."""
    cart = get_cart()

    if not cart.items:
        return "Your cart is empty. Add some items before checking out."

    orders = cart.checkout()
    return cart.format_orders(orders)


def remove_from_cart(item_name: str) -> str:
    """Remove an item from the cart by name.

    Args:
        item_name: Name of the item to remove
    """
    cart = get_cart()
    item_name_lower = item_name.lower()

    for item in cart.items:
        if item_name_lower in item.name.lower():
            cart.remove_item(item.id)
            return f"Removed '{item.name}' from cart."

    return f"Item '{item_name}' not found in cart."


# Create the concierge agent
SYSTEM_INSTRUCTION = """You are a helpful Purchasing Concierge that helps users shop across multiple vendors.

You have access to the following vendors (use discover_vendors to see current availability):
1. Bella's Italian Restaurant - Italian food (pizza, pasta, appetizers, desserts)
2. TechZone Electronics - Consumer electronics (phones, laptops, headphones, accessories)
3. Wanderlust Travel - Travel booking (flights, hotels, vacation packages)

Your responsibilities:
1. Help users discover what vendors are available
2. Route user requests to the appropriate vendor using query_vendor
3. Help users add items to their cart
4. Show cart contents and help with checkout

Workflow:
- When a user asks about food, query the restaurant vendor
- When a user asks about electronics, query the electronics vendor
- When a user asks about travel, query the travel vendor
- Use the responses from vendors to help users make decisions
- Add items to cart when users want to purchase something
- Complete checkout when users are ready to buy

Always be helpful and guide users through the shopping process. If unsure which vendor to use,
ask the user or use discover_vendors to show available options.

Important: When adding items to cart, extract the correct price from the vendor's response.
"""

# List of tools
TOOLS = [
    discover_vendors,
    query_vendor,
    add_to_cart,
    view_cart,
    checkout,
    remove_from_cart,
]


# Lazy agent initialization
_agent_instance = None
_session_service = None

APP_NAME = "purchasing_concierge"


def get_session_service() -> InMemorySessionService:
    """Get or create the session service (lazy initialization)."""
    global _session_service
    if _session_service is None:
        _session_service = InMemorySessionService()
    return _session_service


def create_concierge_agent() -> LlmAgent:
    """Create the concierge agent."""
    # ADK uses environment variables for Vertex AI configuration:
    # GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION
    return LlmAgent(
        name="purchasing_concierge",
        model="gemini-2.0-flash-001",
        instruction=SYSTEM_INSTRUCTION,
        tools=TOOLS,
    )


def get_concierge_agent() -> LlmAgent:
    """Get or create the concierge agent (lazy initialization)."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_concierge_agent()
    return _agent_instance


async def process_message(
    message: str,
    session_id: str = "default",
    event_callback: Optional[EventCallback] = None
) -> str:
    """Process a user message and return the concierge's response.

    Args:
        message: The user's message to process
        session_id: Session ID for conversation history
        event_callback: Optional callback to receive UI events
    """
    # Set up event callback if provided
    if event_callback is not None:
        set_event_callback(event_callback)

    # Emit processing start event
    emit_event(create_event(
        EventType.PROCESSING_START,
        message=message,
    ))

    agent = get_concierge_agent()
    session_service = get_session_service()

    # Create session if it doesn't exist
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

    response_text = ""
    try:
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
                        chunk = part.text
                        response_text += chunk
                        # Emit response chunk event
                        emit_event(create_event(
                            EventType.RESPONSE_CHUNK,
                            message=chunk,
                            full_response=response_text,
                        ))

        # Emit response complete event
        emit_event(create_event(
            EventType.RESPONSE_COMPLETE,
            message=response_text,
        ))

    except Exception as e:
        # Emit error event
        emit_event(create_event(
            EventType.ERROR,
            message=str(e),
        ))
        return f"Error processing your request: {str(e)}"

    return response_text if response_text else "I'm sorry, I couldn't process your request."


async def interactive_session():
    """Run an interactive CLI session with the concierge."""
    print("\n" + "=" * 60)
    print("  Welcome to the A2A Marketplace Concierge!")
    print("=" * 60)
    print("\nI can help you shop across multiple vendors:")
    print("  • Italian Restaurant (food)")
    print("  • Electronics Store (tech)")
    print("  • Travel Agency (trips)")
    print("\nType 'quit' to exit, 'cart' to view cart, 'checkout' to complete purchase")
    print("-" * 60 + "\n")

    session_id = str(uuid.uuid4())

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("\nThank you for shopping with us! Goodbye!")
                break

            response = await process_message(user_input, session_id)
            print(f"\nConcierge: {response}\n")

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
