"""
Main RAG system integrating all components
"""
from src.config import Config
from src.document_processor import DocumentProcessor
from src.vector_store import VectorStore
from src.gemini_generator import GeminiGenerator
from typing import List, Dict

class RAGSystem:
    """Retrieval-Augmented Generation system for Marmara University CENG Department"""
    
    def __init__(self):
        """Initialize RAG system"""
        Config.validate()
        
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.generator = GeminiGenerator()
    
    def load_documents(self, directory: str):
        """
        Load and index documents from directory
        
        Args:
            directory: Path to directory containing documents
        """
        print(f"Loading documents from {directory}...")
        
        # Load documents
        documents = self.document_processor.load_documents_from_directory(directory)
        print(f"Loaded {len(documents)} documents")
        
        # Process and chunk documents
        processed_docs = self.document_processor.process_documents(documents)
        print(f"Created {len(processed_docs)} chunks")
        
        # Add to vector store
        self.vector_store.add_documents(processed_docs)
        print(f"Indexed documents. Total documents in store: {self.vector_store.get_collection_count()}")
    
    def query(self, question: str, top_k: int = None) -> Dict[str, any]:
        """
        Query the RAG system
        
        Args:
            question: User question
            top_k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer and retrieved documents
        """
        print(f"\nProcessing query: {question}")
        
        # Retrieve relevant documents
        retrieved_docs = self.vector_store.search(question, top_k)
        print(f"Retrieved {len(retrieved_docs)} relevant documents")
        
        # Generate response
        answer = self.generator.generate_response(question, retrieved_docs)
        
        return {
            'question': question,
            'answer': answer,
            'retrieved_documents': retrieved_docs
        }
    
    def add_document(self, content: str, source: str):
        """
        Add a single document to the system
        
        Args:
            content: Document content
            source: Document source/name
        """
        doc = {'content': content, 'source': source, 'metadata': {'source': source}}
        processed_docs = self.document_processor.process_documents([doc])
        self.vector_store.add_documents(processed_docs)
    
    def get_stats(self) -> Dict[str, any]:
        """
        Get system statistics
        
        Returns:
            Dictionary with system statistics
        """
        return {
            'total_documents': self.vector_store.get_collection_count(),
            'collection_name': Config.COLLECTION_NAME,
            'model': Config.GEMINI_MODEL
        }
