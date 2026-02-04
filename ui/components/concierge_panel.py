"""Concierge panel component (left side)."""

import streamlit as st
from typing import List, Dict, Any
from datetime import datetime


def render_concierge_panel(
    messages: List[Dict[str, str]],
    events: List[Dict[str, Any]],
    current_response: str = "",
    processing: bool = False,
) -> None:
    """Render the concierge chat panel (left side)."""
    st.markdown("### 💭 Concierge Reasoning")
    st.markdown("---")

    # Create a container for chat messages
    chat_container = st.container()

    with chat_container:
        # Render chat messages
        for msg in messages:
            role = msg.get("role", "user")

            if role == "user":
                with st.chat_message("user"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.markdown(msg["content"])

        # Show current streaming response if processing
        if processing and current_response:
            with st.chat_message("assistant"):
                st.markdown(current_response + "▌")

    # Render processing milestones
    if events:
        st.markdown("---")
        st.markdown("#### Processing Timeline")

        for event in events[-10:]:  # Show last 10 events
            icon = event.get("icon", "•")
            message = event.get("message", "")
            timestamp = event.get("timestamp", "")
            duration_ms = event.get("duration_ms")

            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M:%S")
            except Exception:
                time_str = ""

            # Build event display
            duration_str = f" ({duration_ms:.0f}ms)" if duration_ms else ""

            event_html = f"""
            <div style="
                padding: 4px 8px;
                margin: 4px 0;
                background: #1E1E1E;
                border-radius: 4px;
                font-size: 13px;
            ">
                <span style="margin-right: 8px;">{icon}</span>
                <span>{message}</span>
                <span style="color: #888; margin-left: 8px;">{time_str}{duration_str}</span>
            </div>
            """
            st.markdown(event_html, unsafe_allow_html=True)

    # Show spinner if processing
    if processing:
        st.markdown("---")
        with st.spinner("Processing..."):
            st.empty()


def render_processing_indicator(message: str = "Processing...") -> None:
    """Render a processing indicator."""
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            padding: 8px 12px;
            background: #1E1E1E;
            border-radius: 8px;
            margin: 8px 0;
        ">
            <div style="
                width: 12px;
                height: 12px;
                background: #FF6B6B;
                border-radius: 50%;
                margin-right: 12px;
                animation: pulse 1.5s infinite;
            "></div>
            <span>{message}</span>
        </div>
        <style>
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
