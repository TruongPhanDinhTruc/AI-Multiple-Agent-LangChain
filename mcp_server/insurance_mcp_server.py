import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="insurance-knowledge")

# Load JSON data
with open("data/insurance_faq.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)


@mcp.tool(
    name="search_knowledge",
    description="Search in insurance knowledge base by keyword"
)
def search_knowledge(query: str):
    q = query.lower()

    results = [
        item for item in DATA
        if q in item["title"].lower()
        or q in item["summary"].lower()
        or q in item["content"].lower()
        or any(q in t.lower() for t in item["tags"])
    ]

    return {"results": results}


@mcp.tool(
    name="get_knowledge_by_category",
    description="Get insurance knowledge article by category"
)
def get_knowledge_by_category(category: str):
    item = next((x for x in DATA if x["category"] == category), None)
    return {"item": item}

if __name__ == "__main__":
    mcp.run(transport="stdio")
