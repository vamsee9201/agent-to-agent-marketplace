"""Base MCP server class for vendor data access."""

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import json
from typing import Any, Callable
import asyncio


class BaseMCPServer:
    """Base class for MCP servers providing data access."""

    def __init__(self, name: str):
        self.name = name
        self.server = Server(name)
        self._tools: dict[str, Callable] = {}
        self._setup_handlers()

    def _setup_handlers(self):
        """Set up MCP protocol handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name=name,
                    description=func.__doc__ or f"Tool: {name}",
                    inputSchema=getattr(func, "_schema", {"type": "object", "properties": {}})
                )
                for name, func in self._tools.items()
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            if name not in self._tools:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

            try:
                result = await self._tools[name](**arguments)
                if isinstance(result, (dict, list)):
                    result = json.dumps(result, indent=2)
                return [TextContent(type="text", text=str(result))]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]

    def tool(self, schema: dict = None):
        """Decorator to register a tool with optional schema."""
        def decorator(func: Callable):
            if schema:
                func._schema = schema
            self._tools[func.__name__] = func
            return func
        return decorator

    def register_tool(self, name: str, func: Callable, schema: dict = None):
        """Register a tool function."""
        if schema:
            func._schema = schema
        self._tools[name] = func

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def create_tool_schema(properties: dict, required: list[str] = None) -> dict:
    """Helper to create a JSON schema for a tool."""
    schema = {
        "type": "object",
        "properties": properties
    }
    if required:
        schema["required"] = required
    return schema
