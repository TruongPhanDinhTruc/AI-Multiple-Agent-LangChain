import asyncio
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Khởi tạo MCP client
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/insurance_mcp_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Khởi tạo session
            await session.initialize()
            
            # Lấy danh sách tools từ MCP server
            tools_list = await session.list_tools()
            print(f"\n✓ Available tools: {[tool.name for tool in tools_list.tools]}\n")
            
            # Test 1: Search knowledge
            print("=== Test 1: Search 'nhân thọ' ===")
            result = await session.call_tool("search_knowledge", {"query": "nhân thọ"})
            print(f"Result: {result.content}\n")
            
            # Test 2: Get categories
            print("=== Test 2: Get all categories ===")
            result = await session.call_tool("get_all_categories", {})
            print(f"Result: {result.content}\n")
            
            # Test 3: Get by category
            print("=== Test 3: Get Life Insurance articles ===")
            result = await session.call_tool("get_knowledge_by_category", 
                                            {"category": "Life Insurance"})
            print(f"Result: {result.content}\n")
            
            # Test 4: Get by ID
            print("=== Test 4: Get article ID=1 ===")
            result = await session.call_tool("get_article_by_id", {"article_id": 1})
            print(f"Result: {result.content}\n")


if __name__ == "__main__":
    asyncio.run(main())