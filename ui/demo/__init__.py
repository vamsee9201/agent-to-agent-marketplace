"""Demo mode for A2A Marketplace."""

from .auto_demo import run_demo, stop_demo
from .scenarios import RESTAURANT_QUICK_DEMO, get_demo_scenario

__all__ = [
    "run_demo",
    "stop_demo",
    "RESTAURANT_QUICK_DEMO",
    "get_demo_scenario",
]
