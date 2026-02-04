"""LangGraph agent for Bella's Italian Restaurant."""

from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import os

from .tools import TOOLS

# Lazy initialization flag
_agent_instance = None


class AgentState(TypedDict):
    """State for the restaurant agent."""
    messages: Annotated[list, add_messages]


# System prompt for the restaurant agent
SYSTEM_PROMPT = """You are a helpful assistant for Bella's Italian Restaurant.
You help customers with:
- Browsing our menu
- Finding dishes by category or name
- Getting recommendations based on dietary preferences
- Providing details about specific dishes
- Helping with food orders

Be friendly, helpful, and knowledgeable about Italian cuisine.
Always use the available tools to get accurate menu information.
When recommending dishes, consider the customer's preferences and dietary restrictions.
"""


def create_restaurant_agent():
    """Create the LangGraph restaurant agent."""

    # Initialize the LLM using Vertex AI
    llm = ChatVertexAI(
        model="gemini-2.0-flash-001",
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )

    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools(TOOLS)

    def should_continue(state: AgentState) -> str:
        """Determine if we should continue or end."""
        messages = state["messages"]
        last_message = messages[-1]

        # If the LLM made a tool call, continue to tools
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"

        # Otherwise, we're done
        return END

    def call_model(state: AgentState) -> dict:
        """Call the LLM with the current state."""
        messages = state["messages"]

        # Add system prompt if not present
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(TOOLS))

    # Set entry point
    workflow.set_entry_point("agent")

    # Add edges
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    return workflow.compile()


def get_restaurant_agent():
    """Get or create the restaurant agent (lazy initialization)."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_restaurant_agent()
    return _agent_instance


async def process_message(message: str, history: list = None) -> str:
    """Process a user message and return the agent's response."""
    messages = []

    # Add history if provided
    if history:
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))

    # Add the new message
    messages.append(HumanMessage(content=message))

    # Run the agent
    agent = get_restaurant_agent()
    result = await agent.ainvoke({"messages": messages})

    # Get the last AI message
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content

    return "I'm sorry, I couldn't process your request."
