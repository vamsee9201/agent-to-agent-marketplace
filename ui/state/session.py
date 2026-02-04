"""Session state management for Streamlit UI."""

import uuid
from datetime import datetime
from typing import Optional, Dict, List, Any

import streamlit as st


def init_session_state() -> None:
    """Initialize all session state variables."""
    defaults = {
        "session_id": str(uuid.uuid4()),
        "messages": [],  # Chat history: [{"role": "user"|"assistant", "content": str}]
        "concierge_events": [],  # Milestones for left panel
        "a2a_exchanges": [],  # JSON exchanges for right panel
        "vendor_status": {},  # {name: is_healthy}
        "demo_running": False,
        "processing": False,
        "last_error": None,
        "current_response": "",  # For streaming response display
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def get_session_id() -> str:
    """Get the current session ID."""
    return st.session_state.get("session_id", "default")


def get_messages() -> List[Dict[str, str]]:
    """Get chat message history."""
    return st.session_state.get("messages", [])


def add_message(role: str, content: str) -> None:
    """Add a message to the chat history."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    st.session_state["messages"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat(),
    })


def get_concierge_events() -> List[Dict[str, Any]]:
    """Get concierge processing events."""
    return st.session_state.get("concierge_events", [])


def add_concierge_event(event_type: str, message: str, **kwargs) -> None:
    """Add a processing milestone event."""
    if "concierge_events" not in st.session_state:
        st.session_state["concierge_events"] = []
    st.session_state["concierge_events"].append({
        "type": event_type,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        **kwargs,
    })


def get_a2a_exchanges() -> List[Dict[str, Any]]:
    """Get A2A protocol exchanges."""
    return st.session_state.get("a2a_exchanges", [])


def add_a2a_exchange(
    direction: str,  # "request" or "response"
    vendor_name: str,
    raw_json: str,
    duration_ms: Optional[float] = None,
) -> None:
    """Add an A2A protocol exchange."""
    if "a2a_exchanges" not in st.session_state:
        st.session_state["a2a_exchanges"] = []
    st.session_state["a2a_exchanges"].append({
        "direction": direction,
        "vendor_name": vendor_name,
        "raw_json": raw_json,
        "duration_ms": duration_ms,
        "timestamp": datetime.now().isoformat(),
    })


def get_vendor_status() -> Dict[str, bool]:
    """Get vendor health status."""
    return st.session_state.get("vendor_status", {})


def set_vendor_status(status: Dict[str, bool]) -> None:
    """Set vendor health status."""
    st.session_state["vendor_status"] = status


def is_processing() -> bool:
    """Check if currently processing a message."""
    return st.session_state.get("processing", False)


def set_processing(value: bool) -> None:
    """Set processing state."""
    st.session_state["processing"] = value


def is_demo_running() -> bool:
    """Check if demo mode is running."""
    return st.session_state.get("demo_running", False)


def set_demo_running(value: bool) -> None:
    """Set demo running state."""
    st.session_state["demo_running"] = value


def get_last_error() -> Optional[str]:
    """Get the last error message."""
    return st.session_state.get("last_error")


def set_last_error(error: Optional[str]) -> None:
    """Set the last error message."""
    st.session_state["last_error"] = error


def get_current_response() -> str:
    """Get the current streaming response."""
    return st.session_state.get("current_response", "")


def set_current_response(response: str) -> None:
    """Set the current streaming response."""
    st.session_state["current_response"] = response


def clear_session() -> None:
    """Clear all session state for a new conversation."""
    st.session_state["session_id"] = str(uuid.uuid4())
    st.session_state["messages"] = []
    st.session_state["concierge_events"] = []
    st.session_state["a2a_exchanges"] = []
    st.session_state["demo_running"] = False
    st.session_state["processing"] = False
    st.session_state["last_error"] = None
    st.session_state["current_response"] = ""

    # Also clear the cart
    try:
        from concierge.cart import get_cart
        cart = get_cart()
        cart.clear()
    except Exception:
        pass
