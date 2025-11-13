from langchain.agents import create_agent
from .base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import MODEL_NAME, TEMPERATURE
from tools.customer_lookup_tool import get_customer_info
from memory.memory_save import memory, config
from langchain_core.messages import HumanMessage, AIMessage

class CustomerAgent(BaseAgent):
    def __init__(self):
        llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=TEMPERATURE)
        tools = [get_customer_info]

        self.agent = create_agent(
            tools=tools,
            model=llm,
            checkpointer=memory
        )

    def handle(self, query: str) -> str:
        message = {"messages": [HumanMessage(content=query)]}
        try:
            result = self.agent.invoke(message, config)
            if isinstance(result, dict) and "error" in result:
                if result["error"] == "customer not found":
                    return "Customer not found"
                if result["error"] == "multiple matches":
                    return "Multiple customers found"
                
            last_message = result["messages"][-1]
            if isinstance(last_message, AIMessage):
                return last_message.content
            if isinstance(last_message, dict):
                return last_message.get("content", "No content")
            return str(last_message)
        except Exception as e:
            return f"Error: {e}"
        
    @staticmethod
    def format_customer_profile(profile: dict) -> str:
        return(
            f"{profile['name']} ({profile['status']})\n"
            f"Email: {profile['email']}\n"
            f"Phone: {profile['phone']}\n"
        )