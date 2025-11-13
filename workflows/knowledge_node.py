from langchain_core.messages import AIMessage
from model.message_state import MessagesState
from agents.knowledge_agent import KnowledgeAgent

knowledge_agent = KnowledgeAgent()
def knowledge_node(state: MessagesState):
    query = state["messages"][-1].content
    result = knowledge_agent.handle(query)
    return {"messages": [AIMessage(content=result)]}