from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated, Any, Dict
from langgraph.graph.message import add_messages

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    orchestration_plan: Dict[str, Any]  # Kế hoạch từ orchestrator
    agent_results: Dict[str, str]  # Kết quả từ từng agent
    final_response: str  # Response cuối cùng