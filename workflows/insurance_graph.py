from langgraph.graph import StateGraph, START, END
from agents.router_agent import RouterAgent
from model.message_state import MessagesState
from workflows.customer_node import customer_node
from workflows.lead_node import lead_node
from workflows.knowledge_node import knowledge_node
from memory.memory_save import memory, config
from langchain_core.messages import HumanMessage, AIMessage

router_agent = RouterAgent()
def router(state: MessagesState):
    query = state["messages"][-1].content
    intent = router_agent.classify_intent(query)
    # Lưu intent nếu bạn muốn
    return {"messages": [AIMessage(content=f"[Router] Intent: {intent}")]}

def route_decision(state: MessagesState):
    query = state["messages"][-1].content
    return router_agent.classify_intent(query)

graph = StateGraph(MessagesState)
graph.add_edge(START, "router")
graph.add_node("router", router)
graph.add_node("customer", customer_node)
graph.add_node("lead", lead_node)
graph.add_node("knowledge", knowledge_node)
graph.add_conditional_edges(
    "router",
    route_decision,
    [ "customer", "lead", "knowledge", END ],
)
graph.add_edge("customer", END)
graph.add_edge("lead", END)
graph.add_edge("knowledge", END)
graph.add_edge("router", END)

app = graph.compile(checkpointer=memory)

class InsuranceWorkflow:
    def __init__(self):
        self.workflow = app

    def run(self, query: str):
        return self.workflow.invoke({"messages": [HumanMessage(content=query)]}, config)