from langchain_community import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import MODEL_NAME, TEMPERATURE

template = PromptTemplate.from_template(
    "Bạn là tư vấn viên bảo hiểm. Câu hỏi: {question}"
)

llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=TEMPERATURE)

def run_chain(question: str):
    prompt = template.format(question=question)
    result = llm.invoke(prompt)
    return result.content