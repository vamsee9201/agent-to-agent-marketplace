"""Main Streamlit application for A2A Marketplace."""

import asyncio
import time
from pathlib import Path

import streamlit as st

# Configure page first (must be first Streamlit command)
st.set_page_config(
    page_title="A2A Marketplace",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import components and state management
from ui.components import (
    render_header,
    render_cart_sidebar,
    render_concierge_panel,
    render_a2a_protocol_panel,
    render_about_section,
    render_error_display,
)
from ui.components.error_display import render_vendor_offline_warning
from ui.components.chat_input import render_quick_actions
from ui.state import (
    init_session_state,
    get_session_id,
    get_messages,
    add_message,
    get_concierge_events,
    get_a2a_exchanges,
    get_vendor_status,
    set_vendor_status,
    is_processing,
    set_processing,
    is_demo_running,
    set_demo_running,
    get_last_error,
    set_last_error,
    clear_session,
    handle_ui_event,
)
from ui.state.session import get_current_response, set_current_response
from ui.demo.auto_demo import (
    run_demo,
    stop_demo,
    get_current_demo_step,
    advance_demo_step,
    get_demo_narration,
    set_demo_narration,
    get_demo_progress,
)


def load_css():
    """Load custom CSS styling."""
    css_path = Path(__file__).parent / "styles" / "dark_theme.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def check_vendor_health():
    """Check health of all vendors and update status."""
    async def _check():
        try:
            from concierge.discovery import get_registry
            registry = await get_registry()
            health = await registry.health_check()
            # Convert URL keys to vendor names
            status = {}
            for url, is_healthy in health.items():
                vendor = registry.vendors.get(url)
                if vendor:
                    status[vendor.name] = is_healthy
            return status
        except Exception as e:
            st.error(f"Failed to check vendor health: {e}")
            return {}

    return asyncio.run(_check())


async def process_message_async(message: str) -> str:
    """Process a message through the concierge agent."""
    from concierge.agent import process_message

    # Set up event callback
    response = await process_message(
        message=message,
        session_id=get_session_id(),
        event_callback=handle_ui_event,
    )
    return response


def handle_user_message(message: str):
    """Handle a user message submission."""
    if not message.strip():
        return

    # Add user message to history
    add_message("user", message)
    set_processing(True)
    set_last_error(None)
    set_current_response("")

    try:
        # Process the message
        response = asyncio.run(process_message_async(message))

        # Add assistant response to history
        add_message("assistant", response)
        set_current_response("")

    except Exception as e:
        set_last_error(str(e))

    finally:
        set_processing(False)


def handle_checkout():
    """Handle checkout action."""
    handle_user_message("Checkout my cart")


def handle_new_conversation():
    """Handle new conversation action."""
    clear_session()
    st.rerun()


def handle_run_demo():
    """Handle demo start action."""
    run_demo("restaurant")
    st.rerun()


def process_demo_step():
    """Process the current demo step if demo is running."""
    if not is_demo_running():
        return

    step = get_current_demo_step()
    if step is None:
        stop_demo()
        return

    # Show narration
    narration = step.get("narration", "")
    if narration:
        set_demo_narration(narration)

    # Process message if present
    message = step.get("message")
    if message:
        handle_user_message(message)

    # Wait and advance
    wait_time = step.get("wait", 2)
    time.sleep(wait_time)

    if not advance_demo_step():
        stop_demo()

    st.rerun()


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()

    # Load custom CSS
    load_css()

    # Check vendor health on first load
    if not get_vendor_status():
        status = check_vendor_health()
        set_vendor_status(status)

    # Get current state
    vendor_status = get_vendor_status()
    messages = get_messages()
    events = get_concierge_events()
    exchanges = get_a2a_exchanges()
    processing = is_processing()
    demo_running = is_demo_running()
    last_error = get_last_error()

    # Render header
    render_header(vendor_status)

    # Check for offline vendors
    offline_vendors = [name for name, healthy in vendor_status.items() if not healthy]
    if offline_vendors:
        render_vendor_offline_warning(offline_vendors)

    # Render about section
    render_about_section()

    # Render demo narration if demo is running
    if demo_running:
        narration = get_demo_narration()
        if narration:
            progress = get_demo_progress()
            st.info(f"🎬 **Demo ({progress[0]}/{progress[1]})**: {narration}")

    # Main content area - two columns
    left_col, right_col = st.columns([1, 1])

    with left_col:
        render_concierge_panel(
            messages=messages,
            events=events,
            current_response=get_current_response(),
            processing=processing,
        )

    with right_col:
        render_a2a_protocol_panel(exchanges)

    # Error display
    if last_error:
        render_error_display(
            error=last_error,
            on_retry=lambda: handle_user_message(messages[-1]["content"] if messages else ""),
            on_dismiss=lambda: set_last_error(None),
        )

    # Quick actions
    if not demo_running and not processing:
        quick_message = render_quick_actions()
        if quick_message:
            handle_user_message(quick_message)
            st.rerun()

    # Chat input
    if prompt := st.chat_input(
        placeholder="Type your message...",
        disabled=demo_running or processing,
    ):
        handle_user_message(prompt)
        st.rerun()

    # Sidebar with cart
    with st.sidebar:
        render_cart_sidebar(
            on_checkout=handle_checkout,
            on_new_conversation=handle_new_conversation,
            on_run_demo=handle_run_demo,
            demo_running=demo_running,
        )

    # Process demo step if running (in separate thread to not block)
    if demo_running and not processing:
        process_demo_step()


if __name__ == "__main__":
    main()
