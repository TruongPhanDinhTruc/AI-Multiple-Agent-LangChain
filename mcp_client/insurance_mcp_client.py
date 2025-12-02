from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio

# Kết nối tới MCP server
client = MultiServerMCPClient(
    {
        "insurance-knowledge": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            # Absolute path to your math_server.py file
            "args": ["mcp_server/insurance_mcp_server.py"],
        }
    }
)

tools = asyncio.run(client.get_tools())
