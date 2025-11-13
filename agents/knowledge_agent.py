import json
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import MODEL_NAME, TEMPERATURE

class KnowledgeAgent():
    def __init__(self):
        with open("data/insurance_faq.json", "r", encoding="utf-8") as f:
            self.faq = json.load(f)
        self.llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=TEMPERATURE)

    def handle(self, query: str) -> str:
        prompt = f"Sử dụng FAQ sau để trả lời: {self.faqs} \n Câu hỏi: {query}"
        res = self.llm.invoke(prompt)
        return res.content