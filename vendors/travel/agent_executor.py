"""A2A Agent Executor for the Travel vendor."""

import uuid
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import TextPart, Message, TaskState, TaskStatus, TaskStatusUpdateEvent
from .agent import process_message


class TravelAgentExecutor(AgentExecutor):
    """A2A executor wrapper for the ADK travel agent."""

    def __init__(self):
        self.conversations: dict[str, list] = {}

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute the agent for an A2A request."""

        # Get the user message from the request
        user_message = self._extract_message(context.message)

        # Get or create conversation history
        context_id = context.context_id or str(uuid.uuid4())
        history = self.conversations.get(context_id, [])

        # Process the message with the ADK agent
        response = await process_message(user_message, history)

        # Update history
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": response})
        self.conversations[context_id] = history

        # Create the response message
        response_message = Message(
            messageId=str(uuid.uuid4()),
            role="agent",
            parts=[TextPart(text=response)]
        )

        # Send the completed task status update event
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=context.task_id,
                context_id=context_id,
                final=True,
                status=TaskStatus(
                    state=TaskState.completed,
                    message=response_message
                )
            )
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """Cancel an ongoing execution."""
        await event_queue.enqueue_event(
            TaskStatus(state=TaskState.canceled)
        )

    def _extract_message(self, message: Message) -> str:
        """Extract text content from an A2A message."""
        if not message or not message.parts:
            return ""

        text_parts = []
        for part in message.parts:
            if isinstance(part, TextPart):
                text_parts.append(part.text)
            elif hasattr(part, 'root') and isinstance(part.root, TextPart):
                text_parts.append(part.root.text)
            elif hasattr(part, 'text'):
                text_parts.append(part.text)

        return " ".join(text_parts)
