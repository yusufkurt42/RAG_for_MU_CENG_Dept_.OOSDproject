"""
Configuration module for RAG system
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for RAG system"""
    
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
    
    # Vector Store Settings
    CHROMA_PERSIST_DIRECTORY = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'marmara_ceng_docs')
    
    # Model Settings
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'models/embedding-001')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    # RAG Settings
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', '3'))
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set. Please set it in .env file")
        return True
