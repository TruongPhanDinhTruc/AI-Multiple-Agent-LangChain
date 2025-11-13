from langgraph.checkpoint.memory import InMemorySaver  
from langchain_core.runnables import RunnableConfig

memory = InMemorySaver()
config: RunnableConfig = {"configurable": {"thread_id": "1"}}
