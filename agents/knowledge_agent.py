from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import MODEL_NAME, TEMPERATURE
from mcp_client.insurance_mcp_client import tools
from memory.memory_save import memory, config
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from rag.rag_agent import InsuranceRAGAgent

class KnowledgeAgent():
    def __init__(self):
        # Initialize RAG agent
        self.rag_agent = InsuranceRAGAgent(
            pdf_path="data/Insurance_Handbook_20103.pdf"
        )
        # Initialize LLM for general conversation
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE
        )

    async def handle(self, query: str) -> str:
        """
        Handle user query with RAG
        """
        try:
            # Query RAG system
            result = await self.rag_agent.query(query)
            
            # Format response with sources
            answer = result["answer"]
            
            # Add source references if available
            # if result["sources"]:
            #     answer += "\n\n📚 References:"
            #     for i, source in enumerate(result["sources"][:3], 1):  # Show top 3 sources
            #         answer += f"\n- Page {source['page']}"
            
            return answer
            
        except Exception as e:
            return f"Đã xảy ra lỗi khi xử lý câu hỏi: {str(e)}"
        
    async def search_handbook(self, query: str, k: int = 5) -> dict:
        """
        Search handbook without generating answer
        """
        try:
            docs = await self.rag_agent.retriever.ainvoke(query)
            
            results = []
            for doc in docs[:k]:
                results.append({
                    "page": doc.metadata.get("page", "Unknown"),
                    "content": doc.page_content
                })
            
            return {
                "query": query,
                "results": results,
                "total": len(results)
            }
            
        except Exception as e:
            return {
                "query": query,
                "results": [],
                "total": 0,
                "error": str(e)
            }