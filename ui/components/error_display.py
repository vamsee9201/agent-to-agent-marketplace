"""Error display component."""

import streamlit as st
from typing import Optional, Callable


def render_error_display(
    error: Optional[str],
    on_retry: Optional[Callable[[], None]] = None,
    on_dismiss: Optional[Callable[[], None]] = None,
) -> None:
    """Render an error message with optional retry button.

    Args:
        error: The error message to display
        on_retry: Optional callback for retry button
        on_dismiss: Optional callback for dismiss button
    """
    if not error:
        return

    st.error(f"**Error:** {error}")

    col1, col2 = st.columns(2)

    with col1:
        if on_retry is not None:
            if st.button("🔄 Retry", key="error_retry", use_container_width=True):
                on_retry()

    with col2:
        if on_dismiss is not None:
            if st.button("✖️ Dismiss", key="error_dismiss", use_container_width=True):
                on_dismiss()


def render_warning_banner(message: str) -> None:
    """Render a warning banner at the top of the page."""
    st.warning(message, icon="⚠️")


def render_vendor_offline_warning(offline_vendors: list[str]) -> None:
    """Render a warning about offline vendors."""
    if not offline_vendors:
        return

    vendor_list = ", ".join(offline_vendors)
    render_warning_banner(
        f"Some vendors are offline: **{vendor_list}**. "
        "Start them with `python -m vendors.<name>` or queries to these vendors will fail."
    )
