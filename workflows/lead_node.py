from model.message_state import MessagesState
from langchain_core.messages import AIMessage
from agents.lead_agent import LeadAgent

lead_agent = LeadAgent()
def lead_node(state: MessagesState):
    """Lead agent node with result tracking"""
    query = state["messages"][0].content
    response = lead_agent.handle(query)

    # Store result
    agent_results = state.get("agent_results", {})
    agent_results["lead"] = response
    return {
        "messages": state["messages"] + [AIMessage(content=response)],
        "agent_results": agent_results
    }