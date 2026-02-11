import asyncio
import os
import sys
import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

# 确保能找到 scripts 文件夹
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)

from scripts.calculator import AirportCalculator

# 初始化服务器
server = Server("IATA-Geo-Core")

# 使用绝对路径加载数据
DATA_PATH = os.path.join(base_path, "data", "iata_geo_core.csv")
calc = AirportCalculator(DATA_PATH)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_airport_distance",
            description="Calculate distance between two IATA airport codes",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "Origin IATA code (e.g. PEK)"},
                    "destination": {"type": "string", "description": "Destination IATA code (e.g. JFK)"},
                },
                "required": ["origin", "destination"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    if name == "get_airport_distance":
        origin = arguments.get("origin", "").upper()
        destination = arguments.get("destination", "").upper()
        distance = calc.calculate_distance(origin, destination)
        if distance is None:
            return [types.TextContent(type="text", text="Error: Airport code not found.")]
        return [types.TextContent(type="text", text=f"Distance: {distance} miles")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="IATA-Geo-Core",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())