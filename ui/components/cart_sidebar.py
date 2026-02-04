"""Cart sidebar component."""

import streamlit as st
from typing import Callable

from ..config import get_vendor_config


def render_cart_sidebar(
    on_checkout: Callable[[], None],
    on_new_conversation: Callable[[], None],
    on_run_demo: Callable[[], None],
    demo_running: bool = False,
) -> None:
    """Render the shopping cart sidebar."""
    try:
        from concierge.cart import get_cart
        cart = get_cart()
    except Exception as e:
        st.error(f"Failed to load cart: {e}")
        return

    st.markdown("### 🛒 Shopping Cart")
    st.markdown("---")

    if not cart.items:
        st.markdown("*Your cart is empty*")
    else:
        # Group items by vendor
        summary = cart.get_summary()

        for vendor_name, vendor_data in summary["vendors"].items():
            config = get_vendor_config(vendor_name)

            st.markdown(f"**{config.emoji} {vendor_name}**")

            for item in vendor_data["items"]:
                st.markdown(
                    f"&nbsp;&nbsp;&nbsp;{item['name']} x{item['quantity']}"
                )
                st.markdown(
                    f"&nbsp;&nbsp;&nbsp;*${item['line_total']:.2f}*"
                )

            st.markdown(f"&nbsp;&nbsp;&nbsp;**Subtotal: ${vendor_data['subtotal']:.2f}**")
            st.markdown("---")

        # Total
        st.markdown(f"### Total: ${summary['total']:.2f}")

        # Checkout button
        if st.button(
            "✅ Checkout",
            key="checkout_btn",
            disabled=demo_running,
            use_container_width=True,
        ):
            on_checkout()

    st.markdown("---")

    # New conversation button
    if st.button(
        "🔄 New Conversation",
        key="new_conv_btn",
        disabled=demo_running,
        use_container_width=True,
    ):
        on_new_conversation()

    st.markdown("---")

    # Demo mode section
    st.markdown("### 🎬 Demo Mode")

    if demo_running:
        st.info("Demo is running...")
        if st.button("⏹️ Stop Demo", key="stop_demo_btn", use_container_width=True):
            st.session_state["demo_running"] = False
            st.rerun()
    else:
        if st.button(
            "▶️ Run Demo (~30s)",
            key="run_demo_btn",
            use_container_width=True,
        ):
            on_run_demo()
