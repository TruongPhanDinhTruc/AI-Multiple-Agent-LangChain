from langgraph.graph import StateGraph, START, END
from agents.orchestrator_agent import OrchestratorAgent
from model.message_state import MessagesState
from workflows.customer_node import customer_node
from workflows.lead_node import lead_node
from workflows.knowledge_node import knowledge_node
from workflows.synthesis_node import synthesis_handler
from memory.memory_save import memory, config
from langchain_core.messages import HumanMessage, AIMessage

class OrchestratorWorkflow:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.graph = self._build_graph()
        self.app = self.graph.compile(checkpointer=memory)
    
    def _build_graph(self):
        """Build orchestrator-based workflow graph"""
        
        graph = StateGraph(MessagesState)
        
        # Add nodes
        graph.add_node("orchestrator", self._orchestrate)
        graph.add_node("customer", customer_node)
        graph.add_node("lead", lead_node)
        graph.add_node("knowledge", knowledge_node)
        graph.add_node("synthesis", synthesis_handler)
        
        # Start -> Orchestrator
        graph.add_edge(START, "orchestrator")
        
        # Orchestrator -> Agent routing
        graph.add_conditional_edges(
            "orchestrator",
            self._route_from_orchestrator,
            {
                "customer": "customer",
                "lead": "lead",
                "knowledge": "knowledge",
                "synthesis": "synthesis",
                "end": END
            }
        )
        
        # Agents -> Decision point
        graph.add_conditional_edges(
            "customer",
            self._check_if_needs_synthesis,
            {
                "synthesis": "synthesis",
                "end": END
            }
        )
        
        graph.add_conditional_edges(
            "lead",
            self._check_if_needs_synthesis,
            {
                "synthesis": "synthesis",
                "end": END
            }
        )
        
        graph.add_conditional_edges(
            "knowledge",
            self._check_if_needs_synthesis,
            {
                "synthesis": "synthesis",
                "end": END
            }
        )
        
        # Synthesis -> End
        graph.add_edge("synthesis", END)
        
        return graph
    
    async def _orchestrate(self, state: MessagesState) -> MessagesState:
        """Orchestrator node - analyze and plan"""
        query = state["messages"][-1].content
        
        # Analyze request
        plan = await self.orchestrator.analyze_request_async(query)
        
        print(f"\n🎯 Orchestration Plan:")
        print(f"  Primary Agent: {plan['primary_agent']}")
        print(f"  Workflow Type: {plan['workflow_type']}")
        print(f"  Reasoning: {plan['reasoning']}")
        print(f"  Needs Synthesis: {plan['needs_synthesis']}\n")
        
        return {
            "messages": state["messages"] + [
                AIMessage(content=f"[Orchestrator] Analyzing request...")
            ],
            "orchestration_plan": plan,
            "agent_results": {}
        }
    
    def _route_from_orchestrator(self, state: MessagesState) -> str:
        """Route to appropriate agent based on orchestration plan"""
        plan = state.get("orchestration_plan", {})
        primary_agent = plan.get("primary_agent", "knowledge")
        
        # For simple workflow, route directly to primary agent
        if plan.get("workflow_type") == "simple":
            return primary_agent
        
        # For complex workflows, might need synthesis
        if plan.get("needs_synthesis"):
            # Execute primary agent first
            return primary_agent
        
        return primary_agent
    
    def _check_if_needs_synthesis(self, state: MessagesState) -> str:
        """Check if synthesis is needed after agent execution"""
        plan = state.get("orchestration_plan", {})
        
        # If there are secondary agents to execute
        secondary_agents = plan.get("secondary_agents", [])
        agent_results = state.get("agent_results", {})
        
        # Check if we need to execute more agents
        executed_agents = len(agent_results)
        total_agents = 1 + len(secondary_agents)  # primary + secondary
        
        if executed_agents < total_agents:
            # More agents to execute - not implemented in this simple version
            return "end"
        
        # If synthesis is needed
        if plan.get("needs_synthesis", False) and len(agent_results) > 1:
            return "synthesis"
        
        return "end"
    
    async def run(self, query: str):
        """Run the orchestrator workflow"""
        result = await self.app.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config
        )
        return result

# Create workflow instance
workflow = OrchestratorWorkflow()