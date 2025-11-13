import json
from langchain.tools import tool
@tool
def lead_filter(criteria: str) -> dict:
    """
    Filter leads based on criteria from lead.json.
    """
    with open("data/leads.json", "r") as f:
        leads = json.load(f)
    
    return [lead for lead in leads if criteria.lower() in lead["interest_area"].lower()]