from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from rag.vector_store import InsuranceVectorStore
from config.settings import MODEL_NAME, TEMPERATURE, TOP_K_RESULTS
from langchain_core.output_parsers import StrOutputParser

class InsuranceRAGAgent:
    def __init__(self, pdf_path: str = "data/Insurance_Handbook_20103.pdf"):
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE
        )
        
        # Initialize vector store
        self.vector_store_manager = InsuranceVectorStore()
        
        # Load or create vector store
        try:
            self.vector_store_manager.load_vector_store()
        except FileNotFoundError:
            print("Vector store not found. Creating new one...")
            self.vector_store_manager.create_vector_store(pdf_path)
            self.vector_store_manager.save_vector_store()
        
        # Create retriever
        self.retriever = self.vector_store_manager.vector_store.as_retriever(
            search_kwargs={"k": TOP_K_RESULTS}
        )
        
        # Create RAG chain
        self.rag_chain = self._create_rag_chain()
    
    def _format_docs(self, docs):
        """Format documents for context"""
        formatted = []
        for i, doc in enumerate(docs):
            page_num = doc.metadata.get('page', 'Unknown')
            formatted.append(f"[Page {page_num}]:\n{doc.page_content}")
        return "\n\n".join(formatted)
    
    def _create_rag_chain(self):
        """Create RetrievalQA chain with custom prompt"""
        
        template = """
        You are a smart and friendly insurance consultant.

        Based on the context below, answer the customer's question in a detailed, accurate and easy-to-understand manner.

        ANSWER RULES:
        1. Use information from the provided context
        2. If you cannot find the information in the context, honestly say "I do not have this information in the database"
        3. End with a question for the customer to interact further
        
        CONTEXT:
        {context}
        
        QUESTION: {question}
        
        ANSWER:
        """
        
        prompt = ChatPromptTemplate.from_template(template)
        
        rag_chain = (
            {
                "context": self.retriever | self._format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain
    
    async def query(self, question: str) -> dict:
        """Query the RAG system"""
        try:
            # Get relevant documents
            relevant_docs = await self.retriever.ainvoke(question)
            
            # Get answer from RAG chain
            answer = await self.rag_chain.ainvoke(question)
            
            # Format sources
            sources = []
            for doc in relevant_docs:
                sources.append({
                    "title": doc.metadata.get("title", "Unknown"),
                    "category": doc.metadata.get("category", "Unknown"),
                    "content_preview": doc.page_content[:200] + "..."
                })
            
            return {
                "answer": answer,
                "sources": sources,
                "num_sources": len(sources)
            }
            
        except Exception as e:
            return {
                "answer": f"Đã xảy ra lỗi: {str(e)}",
                "sources": [],
                "num_sources": 0
            }
    
    def query_sync(self, question: str) -> dict:
        """Synchronous version of query"""
        try:
            # Get relevant documents
            relevant_docs = self.retriever.invoke(question)
            
            # Get answer from RAG chain
            answer = self.rag_chain.invoke(question)
            
            # Format sources
            sources = []
            for doc in relevant_docs:
                sources.append({
                    "title": doc.metadata.get("title", "Unknown"),
                    "category": doc.metadata.get("category", "Unknown"),
                    "content_preview": doc.page_content[:200] + "..."
                })
            
            return {
                "answer": answer,
                "sources": sources,
                "num_sources": len(sources)
            }
            
        except Exception as e:
            return {
                "answer": f"Đã xảy ra lỗi: {str(e)}",
                "sources": [],
                "num_sources": 0
            }