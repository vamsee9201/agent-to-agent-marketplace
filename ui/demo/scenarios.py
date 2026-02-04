"""Demo scenarios for automated walkthroughs."""

from typing import List, Dict, Any


# Restaurant quick demo scenario (~30 seconds)
RESTAURANT_QUICK_DEMO: List[Dict[str, Any]] = [
    {
        "narration": "Welcome to the A2A Marketplace demo! Let's explore how AI agents communicate.",
        "wait": 4,
    },
    {
        "narration": "First, let's ask the Restaurant vendor about their menu...",
        "message": "What pizzas do you have?",
        "wait": 8,
    },
    {
        "narration": "Notice the A2A JSON on the right - that's the actual protocol exchange!",
        "wait": 4,
    },
    {
        "narration": "Now let's add something to our cart...",
        "message": "Add a Margherita pizza to my cart",
        "wait": 6,
    },
    {
        "narration": "Great! The cart updated. Let's check it...",
        "message": "Show my cart",
        "wait": 4,
    },
    {
        "narration": "Now let's complete the purchase...",
        "message": "Checkout",
        "wait": 4,
    },
    {
        "narration": "Demo complete! You've seen A2A protocol in action. Try your own queries!",
        "wait": 3,
    },
]


# Full marketplace demo (covers all vendors)
FULL_MARKETPLACE_DEMO: List[Dict[str, Any]] = [
    {
        "narration": "Welcome! This demo showcases the A2A Marketplace with three vendor agents.",
        "wait": 4,
    },
    {
        "narration": "Let's start by discovering what vendors are available...",
        "message": "What vendors do you have?",
        "wait": 6,
    },
    {
        "narration": "We have Restaurant (LangGraph), Electronics (CrewAI), and Travel (ADK).",
        "wait": 3,
    },
    {
        "narration": "Let's try the Restaurant...",
        "message": "What Italian dishes can I order?",
        "wait": 8,
    },
    {
        "narration": "Now let's check out the Electronics store...",
        "message": "Show me your best laptops",
        "wait": 8,
    },
    {
        "narration": "And finally, the Travel agency...",
        "message": "I want to plan a trip to Paris",
        "wait": 8,
    },
    {
        "narration": "Each vendor uses a different AI framework, but they all speak A2A!",
        "wait": 3,
    },
    {
        "narration": "Demo complete! Try mixing vendors in your own shopping session.",
        "wait": 3,
    },
]


# Electronics focused demo
ELECTRONICS_DEMO: List[Dict[str, Any]] = [
    {
        "narration": "Let's explore the Electronics vendor powered by CrewAI...",
        "wait": 3,
    },
    {
        "narration": "Asking about available products...",
        "message": "What phones do you have?",
        "wait": 8,
    },
    {
        "narration": "Let's get more details on a specific product...",
        "message": "Tell me more about the iPhone",
        "wait": 6,
    },
    {
        "narration": "Adding to cart...",
        "message": "Add an iPhone to my cart",
        "wait": 5,
    },
    {
        "narration": "Demo complete!",
        "wait": 2,
    },
]


def get_demo_scenario(name: str = "restaurant") -> List[Dict[str, Any]]:
    """Get a demo scenario by name.

    Args:
        name: Name of the scenario ("restaurant", "full", "electronics")

    Returns:
        List of demo steps
    """
    scenarios = {
        "restaurant": RESTAURANT_QUICK_DEMO,
        "full": FULL_MARKETPLACE_DEMO,
        "electronics": ELECTRONICS_DEMO,
    }

    return scenarios.get(name, RESTAURANT_QUICK_DEMO)
