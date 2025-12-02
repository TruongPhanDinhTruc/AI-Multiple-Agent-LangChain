
from agents.customer_agent import CustomerAgent
from model.message_state import MessagesState
from langchain_core.messages import AIMessage

customer_agent = CustomerAgent()
def customer_node(state: MessagesState):
    """Customer agent node with result tracking"""
    query = state["messages"][0].content
    response = customer_agent.handle(query)

    # Store result
    agent_results = state.get("agent_results", {})
    agent_results["customer"] = response
    return {
        "messages": state["messages"] + [AIMessage(content=response)],
        "agent_results": agent_results
    }