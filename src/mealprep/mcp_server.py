import logging
import sys
import os
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from mealprep.services.meal_service import MealService

# Set up logging to a file so we can debug
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.expanduser("~/mealprep_mcp.log")),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger(__name__)

logger.info("MCP Server starting...")

# Initialize your service
service = MealService()

# Create MCP server
server = Server("mealprep")


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """List available resources."""
    return [
        types.Resource(
            uri="mealprep://recipes",
            name="Recipe Database",
            mimeType="application/json",
            description="Access to 2M+ recipes",
        ),
        types.Resource(
            uri="mealprep://meal-plans",
            name="Saved Meal Plans",
            mimeType="application/json",
            description="Your saved meal plans",
        ),
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource."""
    if uri == "mealprep://recipes":
        # Return sample recipes or search results
        recipes = service.vector_store.get_diverse_recipes(limit=10)
        return recipes.to_json()

    elif uri == "mealprep://meal-plans":
        # Return latest meal plan
        plan = service.get_latest_plan()
        return str(plan)

    raise ValueError(f"Unknown resource: {uri}")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="suggest_meal",
            description="Generate a meal suggestion based on ingredients",
            inputSchema={
                "type": "object",
                "properties": {
                    "ingredients": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Available ingredients",
                    },
                    "num_people": {
                        "type": "integer",
                        "description": "Number of people to serve",
                    },
                    "dietary_preferences": {
                        "type": "string",
                        "description": "Dietary restrictions",
                    },
                },
                "required": ["ingredients"],
            },
        ),
        types.Tool(
            name="generate_meal_plan",
            description="Generate a multi-day meal plan",
            inputSchema={
                "type": "object",
                "properties": {
                    "num_days": {
                        "type": "integer",
                        "description": "Number of days for the plan",
                    },
                    "num_people": {
                        "type": "integer",
                        "description": "Number of people",
                    },
                },
            },
        ),
        types.Tool(
            name="search_recipes",
            description="Search for recipes by ingredients or name",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Execute a tool."""
    if name == "suggest_meal":
        result = service.suggest_meal(
            ingredients=arguments.get("ingredients", []),
            num_people=arguments.get("num_people", 2),
            dietary_preferences=arguments.get("dietary_preferences"),
        )
        return [types.TextContent(type="text", text=str(result))]

    elif name == "generate_meal_plan":
        result = service.generate_meal_plan(
            num_days=arguments.get("num_days", 7),
            num_people=arguments.get("num_people", 2),
        )
        return [types.TextContent(type="text", text=str(result))]

    elif name == "search_recipes":
        # Implement recipe search
        query = arguments.get("query", "")
        results = service.vector_store.search(query, limit=5)
        return [types.TextContent(type="text", text=results.to_json())]

    raise ValueError(f"Unknown tool: {name}")


async def main():
    logger.info("Entering main function")
    try:
        async with stdio_server() as (read_stream, write_stream):
            logger.info("stdio_server context established")
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        raise
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
