
from agents.customer_agent import CustomerAgent
from model.message_state import MessagesState
from langchain_core.messages import AIMessage

customer_agent = CustomerAgent()
def customer_node(state: MessagesState):
    query = state["messages"][-1].content
    result = customer_agent.handle(query)
    return {"messages": [AIMessage(content=result)]}