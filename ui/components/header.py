"""Header component with vendor status badges."""

import streamlit as st
from typing import Dict

from ..config import VENDORS, get_vendor_config


def render_header(vendor_status: Dict[str, bool]) -> None:
    """Render the header with title and vendor status badges."""
    # Create header columns
    title_col, status_col = st.columns([1, 2])

    with title_col:
        st.markdown("# 🛒 A2A Marketplace")

    with status_col:
        # Render vendor status badges using columns for better compatibility
        badge_cols = st.columns(len(VENDORS))

        for i, (key, config) in enumerate(VENDORS.items()):
            # Find matching vendor in status (case-insensitive)
            is_healthy = False
            for vendor_name, healthy in vendor_status.items():
                if key in vendor_name.lower():
                    is_healthy = healthy
                    break

            status_dot = "🟢" if is_healthy else "🔴"

            with badge_cols[i]:
                st.markdown(
                    f"{status_dot}{config.emoji} **{config.name}** *{config.framework}*"
                )


def render_vendor_badge(vendor_name: str, is_healthy: bool) -> str:
    """Render a single vendor badge as markdown."""
    config = get_vendor_config(vendor_name)
    status_dot = "🟢" if is_healthy else "🔴"
    return f"{status_dot}{config.emoji} **{config.name}** *{config.framework}*"
