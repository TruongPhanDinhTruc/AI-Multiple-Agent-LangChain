from .base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import MODEL_NAME, TEMPERATURE
from tools.lead_filter import lead_filter
from memory.memory_save import memory, config
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent

class LeadAgent(BaseAgent):
    def __init__(self):
        llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=TEMPERATURE)
        tools = [lead_filter]

        self.agent = create_agent(
            tools=tools,
            model=llm,
            checkpointer=memory
        )

    def handle(self, query: str) -> str:
        message = {"messages": [HumanMessage(content=query)]}
        try:
            result = self.agent.invoke(message, config)
                
            last_message = result["messages"][-1]
            if isinstance(last_message, AIMessage):
                return last_message.content
            if isinstance(last_message, dict):
                return last_message.get("content", "No content")
            return str(last_message)
        except Exception as e:
            return f"Error: {e}"