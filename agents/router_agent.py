from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import MODEL_NAME, TEMPERATURE

class RouterAgent():
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=TEMPERATURE)
    
    def classify_intent(self, query: str) -> str:
        prompt = f"""
        Phân loại câu hỏi thành: customer, lead hoặc knowledge.
        Câu hỏi: {query}
        Trả lời duy nhất một từ: customer, lead, hoặc knowledge.
        """
        res = self.llm.invoke(prompt)
        intent = (res.content or "").strip().lower()
        if "customer" in intent:
            return "customer"
        if "lead" in intent:
            return "lead"
        if "knowledge" in intent:
            return "knowledge"
        return "unknown"
    