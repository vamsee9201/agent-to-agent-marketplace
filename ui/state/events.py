"""Event callback bridge for UI updates."""

from typing import Any
import streamlit as st

from concierge.events import UIEvent, EventType
from .session import (
    add_concierge_event,
    add_a2a_exchange,
    set_current_response,
    set_last_error,
)


def handle_ui_event(event: UIEvent) -> None:
    """Handle UI events from the concierge agent.

    This function is called by the concierge agent during processing
    to update the UI with real-time status information.
    """
    event_type = event.type

    if event_type == EventType.PROCESSING_START:
        add_concierge_event(
            "processing_start",
            f"Processing: \"{event.message}\"",
            icon="🔄",
        )

    elif event_type == EventType.TOOL_CALL_START:
        tool_name = event.data.get("tool_name", "unknown")
        add_concierge_event(
            "tool_call",
            f"Calling tool: {tool_name}",
            icon="🔧",
            vendor_name=event.vendor_name,
        )

    elif event_type == EventType.VENDOR_QUERY_START:
        add_concierge_event(
            "vendor_query_start",
            f"Querying {event.vendor_name}...",
            icon="📡",
            vendor_name=event.vendor_name,
        )

    elif event_type == EventType.VENDOR_QUERY_END:
        add_concierge_event(
            "vendor_query_end",
            f"Got response from {event.vendor_name}",
            icon="✅",
            vendor_name=event.vendor_name,
            duration_ms=event.duration_ms,
        )

    elif event_type == EventType.A2A_REQUEST:
        if event.raw_json:
            add_a2a_exchange(
                direction="request",
                vendor_name=event.vendor_name or "Unknown",
                raw_json=event.raw_json,
            )

    elif event_type == EventType.A2A_RESPONSE:
        if event.raw_json:
            add_a2a_exchange(
                direction="response",
                vendor_name=event.vendor_name or "Unknown",
                raw_json=event.raw_json,
                duration_ms=event.duration_ms,
            )

    elif event_type == EventType.RESPONSE_CHUNK:
        # Update streaming response
        full_response = event.data.get("full_response", event.message)
        set_current_response(full_response)

    elif event_type == EventType.RESPONSE_COMPLETE:
        add_concierge_event(
            "response_complete",
            "Response complete",
            icon="✅",
        )

    elif event_type == EventType.ERROR:
        set_last_error(event.message)
        add_concierge_event(
            "error",
            f"Error: {event.message}",
            icon="❌",
        )
