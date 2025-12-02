from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
from model.message_state import MessagesState
from config.settings import MODEL_NAME, TEMPERATURE

class SynthesisNode:
    """
    Synthesis Node - Aggregate results from multiple agents
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE
        )
    
    async def synthesize(self, state: MessagesState) -> MessagesState:
        """Synthesize results from multiple agents"""
        
        agent_results = state.get("agent_results", {})
        original_query = state["messages"][0].content
        
        if not agent_results:
            return {
                "messages": state["messages"] + [
                    AIMessage(content="Không có kết quả để tổng hợp.")
                ],
                "final_response": "Không có kết quả để tổng hợp."
            }
        
        # Create synthesis prompt
        prompt = ChatPromptTemplate.from_template("""
        You are an expert at synthesizing information.

        ORIGINAL REQUEST: {query}

        RESULTS FROM AGENTS:
        {results}

        Synthesize the above information into a coherent, complete, and easy-to-understand answer.
        Make sure:
        1. Do not miss important information
        2. Eliminate duplicate information
        3. Organize logically, easy to read
        4. Use a friendly, professional tone
        """)
        
        # Format results
        results_text = "\n\n".join([
            f"[{agent.upper()}]:\n{result}"
            for agent, result in agent_results.items()
        ])
        
        # Generate synthesis
        response = await self.llm.ainvoke(
            prompt.format_messages(
                query=original_query,
                results=results_text
            )
        )
        
        final_response = response.content
        
        return {
            "messages": state["messages"] + [AIMessage(content=final_response)],
            "final_response": final_response
        }

synthesis_node = SynthesisNode()

async def synthesis_handler(state: MessagesState) -> MessagesState:
    """Handler for synthesis node"""
    return await synthesis_node.synthesize(state)