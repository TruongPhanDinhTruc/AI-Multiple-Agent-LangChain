from model.message_state import MessagesState
from langchain_core.messages import AIMessage
from agents.lead_agent import LeadAgent

lead_agent = LeadAgent()
def lead_node(state: MessagesState):
    query = state["messages"][-1].content
    result = lead_agent.handle(query)
    return {"messages": [AIMessage(content=result)]}