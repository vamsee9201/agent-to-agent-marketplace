"""CrewAI Crew for TechZone Electronics."""

import os
from crewai import Crew, Process
from .agents import create_electronics_agent
from .tasks import create_response_task


class ElectronicsCrew:
    """Crew for handling electronics customer inquiries."""

    def __init__(self):
        self.agent = create_electronics_agent()

    def process_query(self, query: str) -> str:
        """Process a customer query and return a response."""

        task = create_response_task(query, self.agent)

        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False,
        )

        result = crew.kickoff()
        return str(result)


# Singleton instance
_crew_instance = None


def get_crew() -> ElectronicsCrew:
    """Get or create the electronics crew singleton."""
    global _crew_instance
    if _crew_instance is None:
        _crew_instance = ElectronicsCrew()
    return _crew_instance


async def process_message(message: str, history: list = None) -> str:
    """Process a user message and return the crew's response."""
    crew = get_crew()

    # Build context from history if available
    context = ""
    if history:
        context = "\n".join([
            f"{'Customer' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in history[-4:]  # Last 4 messages for context
        ])
        context = f"Previous conversation:\n{context}\n\n"

    full_query = context + message if context else message

    try:
        response = crew.process_query(full_query)
        return response
    except Exception as e:
        return f"I apologize, but I encountered an issue: {str(e)}. Please try again."
