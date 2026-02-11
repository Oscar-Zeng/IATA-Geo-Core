import asyncio
import os
import sys
import logging

# --- Critical Setup: Logging Configuration ---
# Configure logging to redirect all logs and errors to stderr.
# This prevents non-JSON messages from polluting the stdout stream, 
# which is reserved for MCP JSON-RPC communication.
logging.basicConfig(level=logging.ERROR, stream=sys.stderr)

import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server

# --- Environment Setup: Path Configuration ---
# Ensure the project root and scripts directory are in the system path.
base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)

# --- Noise Isolation: Silent Imports ---
# Some libraries may print initialization messages to stdout.
# We temporarily redirect stdout to stderr during imports to keep the pipe clean.
try:
    _original_stdout = sys.stdout
    sys.stdout = sys.stderr
    from scripts.calculator import AirportCalculator
finally:
    sys.stdout = _original_stdout

# Initialize the MCP Server
server = Server("IATA-Geo-Core")

# Define path to the airport database
DATA_PATH = os.path.join(base_path, "data", "iata_geo_core.csv")

# Initialize the calculator engine with error handling
try:
    calc = AirportCalculator(DATA_PATH)
except Exception as e:
    logging.error(f"Failed to initialize AirportCalculator: {e}")
    calc = None

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for the AI agent."""
    return [
        types.Tool(
            name="get_airport_distance",
            description="Calculate the Great Circle distance between two airports using 3-letter IATA codes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string", 
                        "description": "Origin IATA code (e.g., PEK, LHR, JFK)"
                    },
                    "destination": {
                        "type": "string", 
                        "description": "Destination IATA code (e.g., SIN, DXB, HND)"
                    },
                },
                "required": ["origin", "destination"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Execute a specific tool based on its name."""
    if name == "get_airport_distance":
        if not calc:
            return [types.TextContent(type="text", text="Error: Data engine failed to initialize.")]
        
        # Normalize inputs to uppercase
        origin = arguments.get("origin", "").upper()
        destination = arguments.get("destination", "").upper()
        
        try:
            distance = calc.calculate_distance(origin, destination)
            if distance is None:
                return [types.TextContent(
                    type="text", 
                    text=f"Error: Could not find coordinates for {origin} or {destination}."
                )]
            
            return [types.TextContent(
                type="text", 
                text=f"The Great Circle distance between {origin} and {destination} is {distance} statute miles."
            )]
        except Exception as e:
            logging.error(f"Calculation error: {e}")
            return [types.TextContent(type="text", text=f"An internal error occurred: {str(e)}")]
            
    raise ValueError(f"Unknown tool: {name}")

async def main():
    """Main entry point: Run the MCP server using STDIO transport."""
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
    # Use unbuffered execution for reliable real-time communication
    asyncio.run(main())