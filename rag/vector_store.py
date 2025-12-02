import json
import os
from typing import List, Dict
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters.base import Document
from rag.embeddings import embedding_manager
from config.settings import VECTOR_STORE_PATH, CHUNK_SIZE, CHUNK_OVERLAP, TOP_K_RESULTS
from langchain_community.document_loaders import PyPDFLoader

class InsuranceVectorStore:
    def __init__(self):
        self.embeddings = embedding_manager.get_embeddings()
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", ".", " ", ""]
        )
    
    def load_pdf(self, pdf_path: str) -> List[Document]:
        """Load and process PDF document"""
        print(f"Loading PDF from {pdf_path}...")
        
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        print(f"Loaded {len(documents)} pages from PDF")
        return documents
    
    def create_vector_store(self, json_path: str):
        """Create FAISS vector store from insurance data"""
        print("Loading insurance knowledge data...")
        documents = self.load_pdf(json_path)
        
        print(f"Splitting {len(documents)} documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks")
        
        print("Creating FAISS vector store...")
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        
        print("Vector store created successfully!")
        return self.vector_store
    
    def save_vector_store(self):
        """Save FAISS index to disk"""
        if self.vector_store is None:
            raise ValueError("Vector store not created yet!")
        
        os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
        self.vector_store.save_local(VECTOR_STORE_PATH)
        print(f"Vector store saved to {VECTOR_STORE_PATH}")
    
    def load_vector_store(self):
        """Load FAISS index from disk"""
        if not os.path.exists(VECTOR_STORE_PATH):
            raise FileNotFoundError(f"Vector store not found at {VECTOR_STORE_PATH}")
        
        print(f"Loading vector store from {VECTOR_STORE_PATH}...")
        self.vector_store = FAISS.load_local(
            VECTOR_STORE_PATH,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print("Vector store loaded successfully!")
        return self.vector_store
    
    def search(self, query: str, k: int = TOP_K_RESULTS) -> List[Document]:
        """Search similar documents"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized!")
        
        results = self.vector_store.similarity_search(query, k=k)
        return results
    
    def search_with_score(self, query: str, k: int = TOP_K_RESULTS) -> List[tuple]:
        """Search with similarity scores"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized!")
        
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results
    
    def add_documents(self, documents: List[Document]):
        """Add new documents to existing vector store"""
        if self.vector_store is None:
            raise ValueError("Vector store not initialized!")
        
        chunks = self.text_splitter.split_documents(documents)
        self.vector_store.add_documents(chunks)
        print(f"Added {len(chunks)} new chunks to vector store")