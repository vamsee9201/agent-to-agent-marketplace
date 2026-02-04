"""CrewAI tasks for TechZone Electronics."""

from crewai import Task, Agent


def create_response_task(query: str, agent: Agent = None) -> Task:
    """Create a task to respond to customer query."""
    return Task(
        description=f"""Respond to the following customer query about electronics:

        Customer Query: {query}

        Instructions:
        1. Understand what the customer is looking for
        2. Use the available tools to get accurate product information
        3. If they want to browse, show them relevant products
        4. If they want to compare, use the compare tool
        5. If they want details, use the product details tool
        6. Always check availability for products they're interested in
        7. Provide a helpful, friendly response

        Be concise but thorough in your response.""",
        expected_output="A helpful response addressing the customer's electronics inquiry",
        agent=agent,
    )
