import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("mealprep-test")


@server.list_tools()
async def list_tools():
    return []


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
