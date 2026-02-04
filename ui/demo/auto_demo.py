"""Auto demo controller for running scripted demonstrations."""

import asyncio
import time
from typing import List, Dict, Any, Callable, Optional

import streamlit as st

from .scenarios import get_demo_scenario


async def run_demo_async(
    scenario: List[Dict[str, Any]],
    process_message: Callable[[str], Any],
    on_narration: Callable[[str], None],
    on_step_complete: Callable[[], None],
    check_stop: Callable[[], bool],
) -> None:
    """Run a demo scenario asynchronously.

    Args:
        scenario: List of demo steps
        process_message: Function to process user messages
        on_narration: Callback for narration updates
        on_step_complete: Callback when a step completes
        check_stop: Function to check if demo should stop
    """
    for step in scenario:
        # Check if demo should stop
        if check_stop():
            break

        # Show narration
        narration = step.get("narration", "")
        if narration:
            on_narration(narration)

        # Send message if present
        message = step.get("message")
        if message:
            await process_message(message)

        # Wait
        wait_time = step.get("wait", 2)
        for _ in range(int(wait_time * 10)):  # Check every 100ms
            if check_stop():
                return
            await asyncio.sleep(0.1)

        on_step_complete()


def run_demo(
    scenario_name: str = "restaurant",
    narration_placeholder: Optional[st.empty] = None,
) -> None:
    """Run a demo scenario (synchronous wrapper for Streamlit).

    This function sets up the demo state and should be called from
    the main app when the demo button is clicked.

    Args:
        scenario_name: Name of the scenario to run
        narration_placeholder: Streamlit placeholder for narration text
    """
    st.session_state["demo_running"] = True
    st.session_state["demo_narration"] = ""
    st.session_state["demo_scenario"] = get_demo_scenario(scenario_name)
    st.session_state["demo_step"] = 0


def stop_demo() -> None:
    """Stop the current demo."""
    st.session_state["demo_running"] = False
    st.session_state["demo_step"] = 0
    st.session_state["demo_narration"] = ""


def get_current_demo_step() -> Optional[Dict[str, Any]]:
    """Get the current demo step."""
    if not st.session_state.get("demo_running", False):
        return None

    scenario = st.session_state.get("demo_scenario", [])
    step_idx = st.session_state.get("demo_step", 0)

    if step_idx >= len(scenario):
        return None

    return scenario[step_idx]


def advance_demo_step() -> bool:
    """Advance to the next demo step.

    Returns:
        True if there are more steps, False if demo is complete
    """
    scenario = st.session_state.get("demo_scenario", [])
    step_idx = st.session_state.get("demo_step", 0)

    if step_idx + 1 >= len(scenario):
        stop_demo()
        return False

    st.session_state["demo_step"] = step_idx + 1
    return True


def get_demo_narration() -> str:
    """Get the current demo narration text."""
    return st.session_state.get("demo_narration", "")


def set_demo_narration(text: str) -> None:
    """Set the demo narration text."""
    st.session_state["demo_narration"] = text


def is_demo_running() -> bool:
    """Check if demo is currently running."""
    return st.session_state.get("demo_running", False)


def get_demo_progress() -> tuple[int, int]:
    """Get demo progress as (current_step, total_steps)."""
    scenario = st.session_state.get("demo_scenario", [])
    step_idx = st.session_state.get("demo_step", 0)
    return (step_idx + 1, len(scenario))
