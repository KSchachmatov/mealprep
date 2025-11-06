import asyncio
import sys
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

# Logging to stderr so Claude can see it
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

server = Server("mealprep")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    logger.info("list_tools called")
    return [
        types.Tool(
            name="hello",
            description="Test tool that says hello",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string", "description": "Your name"}},
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Execute a tool."""
    logger.info(f"call_tool: {name} with {arguments}")

    if name == "hello":
        user_name = arguments.get("name", "World")
        return [
            types.TextContent(
                type="text", text=f"Hello, {user_name}! MealPrep MCP server is working!"
            )
        ]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    logger.info("Starting MCP server...")
    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Server connected")
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
