"""Chat input component."""

import streamlit as st
from typing import Callable, Optional


def render_chat_input(
    on_submit: Callable[[str], None],
    disabled: bool = False,
    placeholder: str = "Type your message...",
) -> Optional[str]:
    """Render the chat input field.

    Args:
        on_submit: Callback function when message is submitted
        disabled: Whether the input is disabled
        placeholder: Placeholder text for the input

    Returns:
        The submitted message, or None if no message was submitted
    """
    # Use Streamlit's built-in chat input
    if prompt := st.chat_input(
        placeholder=placeholder,
        disabled=disabled,
        key="chat_input",
    ):
        on_submit(prompt)
        return prompt

    return None


def render_quick_actions() -> Optional[str]:
    """Render quick action buttons for common queries."""
    st.markdown("**Quick Actions:**")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🍕 View Menu", key="qa_menu", use_container_width=True):
            return "What pizzas do you have?"

    with col2:
        if st.button("📱 Browse Tech", key="qa_tech", use_container_width=True):
            return "Show me your best phones"

    with col3:
        if st.button("✈️ Plan Trip", key="qa_trip", use_container_width=True):
            return "I want to book a trip to Paris"

    with col4:
        if st.button("🛒 View Cart", key="qa_cart", use_container_width=True):
            return "Show my cart"

    return None
