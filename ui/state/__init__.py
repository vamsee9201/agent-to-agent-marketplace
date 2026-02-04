"""State management for the UI."""

from .session import (
    init_session_state,
    get_session_id,
    get_messages,
    add_message,
    get_concierge_events,
    add_concierge_event,
    get_a2a_exchanges,
    add_a2a_exchange,
    get_vendor_status,
    set_vendor_status,
    is_processing,
    set_processing,
    is_demo_running,
    set_demo_running,
    get_last_error,
    set_last_error,
    clear_session,
)

from .events import handle_ui_event

__all__ = [
    "init_session_state",
    "get_session_id",
    "get_messages",
    "add_message",
    "get_concierge_events",
    "add_concierge_event",
    "get_a2a_exchanges",
    "add_a2a_exchange",
    "get_vendor_status",
    "set_vendor_status",
    "is_processing",
    "set_processing",
    "is_demo_running",
    "set_demo_running",
    "get_last_error",
    "set_last_error",
    "clear_session",
    "handle_ui_event",
]
