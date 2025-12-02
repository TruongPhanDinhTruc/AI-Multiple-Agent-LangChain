from langchain_core.messages import AIMessage
from model.message_state import MessagesState
from agents.knowledge_agent import KnowledgeAgent

knowledge_agent = KnowledgeAgent()
async def knowledge_node(state: MessagesState):
    """Knowledge agent node with result tracking"""
    query = state["messages"][0].content  # Original query
    
    # Get response from knowledge agent
    response = await knowledge_agent.handle(query)
    
    # Store result
    agent_results = state.get("agent_results", {})
    agent_results["knowledge"] = response
    
    return {
        "messages": state["messages"] + [AIMessage(content=response)],
        "agent_results": agent_results
    }