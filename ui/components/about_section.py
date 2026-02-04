"""About section component."""

import streamlit as st


def render_about_section() -> None:
    """Render the expandable about section."""
    with st.expander("ℹ️ About A2A Marketplace", expanded=False):
        st.markdown("""
        ## Welcome to the A2A Marketplace Demo!

        This application demonstrates **Agent-to-Agent (A2A)** communication using
        Google's open protocol for AI agent interoperability.

        ### What is A2A?

        The **Agent2Agent (A2A) Protocol** is an open standard that enables AI agents
        built on different frameworks to communicate and collaborate seamlessly.
        Think of it as a universal translator for AI agents.

        ### The Vendors

        This demo features three vendor agents, each built with a different AI framework:

        | Vendor | Framework | What They Offer |
        |--------|-----------|-----------------|
        | 🍕 **Restaurant** | LangGraph | Italian cuisine - pizzas, pasta, desserts |
        | 📱 **Electronics** | CrewAI | Tech products - phones, laptops, accessories |
        | ✈️ **Travel** | ADK | Travel services - flights, hotels, packages |

        ### How It Works

        1. **You** send a message to the **Concierge** (the orchestrating agent)
        2. The Concierge determines which **Vendor** can help
        3. The Concierge sends an **A2A request** to the Vendor
        4. The Vendor processes and returns an **A2A response**
        5. You see the results in the chat!

        ### The Two Panels

        - **Left Panel (Concierge Reasoning)**: Shows the chat conversation and
          processing milestones with timestamps
        - **Right Panel (A2A Protocol)**: Shows the actual JSON-RPC messages
          exchanged between agents

        ### Try These Commands

        - "What pizzas do you have?"
        - "Add a Margherita pizza to my cart"
        - "Show me laptops under $1000"
        - "I want to plan a trip to Paris"
        - "View my cart"
        - "Checkout"

        ### Running the Demo

        Click **"Run Demo"** in the sidebar to see an automated walkthrough
        of the A2A protocol in action!
        """)
