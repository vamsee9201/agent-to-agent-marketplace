"""A2A Protocol panel component (right side)."""

import json
import streamlit as st
from typing import List, Dict, Any

from ..config import get_vendor_config, A2A_FIELD_DESCRIPTIONS


def render_a2a_protocol_panel(exchanges: List[Dict[str, Any]]) -> None:
    """Render the A2A protocol exchange panel (right side)."""
    st.markdown("### 🔗 A2A Protocol Exchange")
    st.markdown("---")

    if not exchanges:
        st.markdown("*No A2A exchanges yet. Send a message to see the protocol in action.*")
        _render_protocol_help()
        return

    # Render exchanges
    for i, exchange in enumerate(exchanges):
        direction = exchange.get("direction", "request")
        vendor_name = exchange.get("vendor_name", "Unknown")
        raw_json = exchange.get("raw_json", "{}")
        duration_ms = exchange.get("duration_ms")

        config = get_vendor_config(vendor_name)

        # Direction indicator
        if direction == "request":
            icon = "📤"
            title = f"Request to {config.emoji} {vendor_name}"
            border_color = config.color
        else:
            icon = "📥"
            duration_str = f" ({duration_ms:.0f}ms)" if duration_ms else ""
            title = f"Response from {config.emoji} {vendor_name}{duration_str}"
            border_color = "#00D26A"

        # Render exchange card
        with st.expander(f"{icon} {title}", expanded=(i >= len(exchanges) - 2)):
            _render_json_with_tooltips(raw_json)


def _render_json_with_tooltips(raw_json: str) -> None:
    """Render JSON with syntax highlighting and field tooltips."""
    try:
        data = json.loads(raw_json)
        formatted = json.dumps(data, indent=2)
    except Exception:
        formatted = raw_json

    # Use code block for JSON display
    st.code(formatted, language="json")

    # Add field descriptions below
    with st.expander("📖 Field Reference", expanded=False):
        try:
            data = json.loads(raw_json)
            relevant_fields = _get_relevant_fields(data)

            for field, desc in relevant_fields.items():
                st.markdown(f"**`{field}`**: {desc}")
        except Exception:
            st.markdown("*Unable to parse JSON*")


def _get_relevant_fields(data: dict, prefix: str = "") -> Dict[str, str]:
    """Get relevant A2A field descriptions for the given data."""
    result = {}

    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key

        # Check for direct match
        if full_key in A2A_FIELD_DESCRIPTIONS:
            result[full_key] = A2A_FIELD_DESCRIPTIONS[full_key]
        elif key in A2A_FIELD_DESCRIPTIONS:
            result[key] = A2A_FIELD_DESCRIPTIONS[key]

        # Recurse into nested dicts
        if isinstance(value, dict):
            nested = _get_relevant_fields(value, full_key)
            result.update(nested)

    return result


def _render_protocol_help() -> None:
    """Render A2A protocol help information."""
    with st.expander("📖 About A2A Protocol", expanded=False):
        st.markdown("""
        **A2A (Agent-to-Agent)** is an open protocol for communication between AI agents.

        **Key Components:**
        - **JSON-RPC 2.0**: Standard request/response format
        - **message/send**: Method for sending messages to agents
        - **Task Status**: Tracks the state of agent processing
        - **Artifacts**: Output data from agent processing

        **Request Format:**
        ```json
        {
          "jsonrpc": "2.0",
          "method": "message/send",
          "params": {
            "message": {"role": "user", "parts": [...]},
            "configuration": {...}
          },
          "id": "<unique-id>"
        }
        ```

        **Response Format:**
        ```json
        {
          "jsonrpc": "2.0",
          "result": {
            "status": {
              "state": "completed",
              "message": {...}
            }
          },
          "id": "<matching-id>"
        }
        ```
        """)


def render_json_card(
    title: str,
    json_data: str,
    direction: str = "request",
    duration_ms: float = None,
) -> None:
    """Render a single JSON exchange card."""
    icon = "📤" if direction == "request" else "📥"
    duration_str = f" ({duration_ms:.0f}ms)" if duration_ms else ""

    with st.expander(f"{icon} {title}{duration_str}", expanded=True):
        _render_json_with_tooltips(json_data)
