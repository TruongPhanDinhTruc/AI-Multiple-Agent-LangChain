from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import MODEL_NAME, TEMPERATURE
from typing import Dict, List
import json

class OrchestratorAgent:
    """
    Orchestrator Agent - Coordinate and decide on workflow
    """
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME,
            temperature=TEMPERATURE
        )
        self.chain = self._create_chain()
    
    def _create_chain(self):
        """Create orchestration chain"""
        
        prompt = ChatPromptTemplate.from_template("""
        You are an Orchestrator Agent - an intelligent coordinator for the insurance system.

        Your task is to analyze the customer's request and decide:
        1. Which agent to process
        2. Order of processing (if multiple agents are needed)
        3. Should results from multiple agents be combined
        4. You can recommend insurance product based on profile user

        AVAILABLE AGENTS:
        - customer: Process customer information, update profile, history
        - lead: Manage new leads, tracking, nurturing
        - knowledge: Answer insurance questions from knowledge base (RAG)

        CUSTOMER REQUEST: {query}

        Return JSON in the format:
        {{
            "primary_agent": "primary agent name",
            "secondary_agents": ["secondary agent if needed"],
            "workflow_type": "simple|sequential|parallel",
            "reasoning": "decision reason",
            "needs_synthesis": true/false
        }}

        RETURN JSON ONLY, NO MORE anything else
        """)
        
        return prompt | self.llm | StrOutputParser()
    
    def analyze_request(self, query: str) -> Dict:
        """Analyze user request and decide workflow"""
        try:
            result = self.chain.invoke({"query": query})
            
            # Parse JSON response
            # Remove markdown code blocks if present
            result = result.strip()
            if result.startswith("```json"):
                result = result[7:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
            
            decision = json.loads(result.strip())
            return decision
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Raw response: {result}")
            # Fallback to knowledge agent
            return {
                "primary_agent": "knowledge",
                "secondary_agents": [],
                "workflow_type": "simple",
                "reasoning": "Fallback due to parse error",
                "needs_synthesis": False
            }
        except Exception as e:
            print(f"Orchestrator error: {e}")
            return {
                "primary_agent": "knowledge",
                "secondary_agents": [],
                "workflow_type": "simple",
                "reasoning": "Fallback due to error",
                "needs_synthesis": False
            }
    
    async def analyze_request_async(self, query: str) -> Dict:
        """Async version of analyze_request"""
        try:
            result = await self.chain.ainvoke({"query": query})
            
            # Clean and parse JSON
            result = result.strip()
            if result.startswith("```json"):
                result = result[7:]
            if result.startswith("```"):
                result = result[3:]
            if result.endswith("```"):
                result = result[:-3]
            
            decision = json.loads(result.strip())
            return decision
            
        except Exception as e:
            print(f"Orchestrator error: {e}")
            return {
                "primary_agent": "knowledge",
                "secondary_agents": [],
                "workflow_type": "simple",
                "reasoning": "Fallback due to error",
                "needs_synthesis": False
            }