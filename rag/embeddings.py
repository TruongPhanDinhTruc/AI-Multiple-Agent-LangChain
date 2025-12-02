from langchain_community.embeddings import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL

class EmbeddingManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            print("🔧 Initializing HuggingFace Embeddings...")
            cls._instance.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL,
                model_kwargs={'device': 'cpu'},  # Đổi 'cuda' nếu có GPU
                encode_kwargs={'normalize_embeddings': True}
            )
            print("✅ Embeddings loaded successfully!")
        return cls._instance
    
    def get_embeddings(self):
        return self.embeddings

# Singleton instance
embedding_manager = EmbeddingManager()