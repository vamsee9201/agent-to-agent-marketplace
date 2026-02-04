"""A2A Agent Executor for the Restaurant vendor."""

import uuid
import logging
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import Part, TextPart, Message, Task, TaskState, TaskStatus, TaskStatusUpdateEvent
from .agent import process_message

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RestaurantAgentExecutor(AgentExecutor):
    """A2A executor wrapper for the LangGraph restaurant agent."""

    def __init__(self):
        self.conversations: dict[str, list] = {}

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute the agent for an A2A request."""
        try:
            logger.info("Starting execute...")

            # Get the user message from the request
            user_message = self._extract_message(context.message)
            logger.info(f"Extracted message: {user_message[:100]}")

            # Get or create conversation history
            context_id = context.context_id or str(uuid.uuid4())
            history = self.conversations.get(context_id, [])

            # Process the message with the LangGraph agent
            logger.info("Processing message with agent...")
            response = await process_message(user_message, history)
            logger.info(f"Got response: {response[:100] if response else 'None'}")

            # Update history
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": response})
            self.conversations[context_id] = history

            # Create the response message
            logger.info("Creating response message...")
            response_message = Message(
                messageId=str(uuid.uuid4()),
                role="agent",
                parts=[TextPart(text=response)]
            )
            logger.info(f"Created message: {response_message}")

            # Send the completed task status update event
            logger.info(f"Sending task status update for task_id={context.task_id}, context_id={context_id}...")
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
            logger.info("Execute completed successfully")
        except Exception as e:
            logger.exception(f"Error in execute: {e}")
            raise

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
