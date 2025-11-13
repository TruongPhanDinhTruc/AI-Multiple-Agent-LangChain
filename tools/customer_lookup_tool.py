import json
from langchain.tools import tool
@tool
def get_customer_info(identifier: str) -> dict:
    """
    Truy xuất thông tin khách hàng theo ID, email hoặc tên.
    Trả về thông tin chi tiết của khách hàng hoặc lỗi nếu không tìm thấy.
    """
    with open("data/customers.json", "r") as f:
        customers = json.load(f)
    
    identifier_lower = identifier.lower().strip()

    matches = [
        cust for cust in customers
        if cust["id"].lower() == identifier_lower or cust["email"].lower() == identifier_lower or cust["name"] == identifier
    ]

    if not matches:
        return {"error": "customer not found"}
    if len(matches) > 1:
        return {"error": "multiple matches", "matches": matches}
    
    return matches[0]