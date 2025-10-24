"""
Vector store for document embeddings using ChromaDB
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict
import google.generativeai as genai
from src.config import Config

class VectorStore:
    """Manage vector embeddings and similarity search"""
    
    def __init__(self):
        """Initialize vector store with ChromaDB"""
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=Config.CHROMA_PERSIST_DIRECTORY
        ))
        
        # Configure Gemini API
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"description": "Marmara University CENG Department documents"}
        )
    
    def add_documents(self, documents: List[Dict[str, str]]):
        """
        Add documents to vector store
        
        Args:
            documents: List of document dictionaries with content and metadata
        """
        if not documents:
            return
        
        # Prepare data for ChromaDB
        ids = [f"{doc['source']}_{doc.get('chunk_id', 0)}" for doc in documents]
        contents = [doc['content'] for doc in documents]
        metadatas = [{'source': doc['source'], 'chunk_id': str(doc.get('chunk_id', 0))} 
                     for doc in documents]
        
        # Generate embeddings using Gemini
        embeddings = self._generate_embeddings(contents)
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas
        )
    
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for texts using Gemini
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            try:
                result = genai.embed_content(
                    model=Config.EMBEDDING_MODEL,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            except Exception as e:
                print(f"Error generating embedding: {e}")
                # Use zero vector as fallback
                embeddings.append([0.0] * 768)
        
        return embeddings
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, str]]:
        """
        Search for relevant documents
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant documents
        """
        if top_k is None:
            top_k = Config.TOP_K_RESULTS
        
        # Generate query embedding
        try:
            result = genai.embed_content(
                model=Config.EMBEDDING_MODEL,
                content=query,
                task_type="retrieval_query"
            )
            query_embedding = result['embedding']
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return []
        
        # Search in collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        # Format results
        documents = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                documents.append({
                    'content': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else 0
                })
        
        return documents
    
    def get_collection_count(self) -> int:
        """Get number of documents in collection"""
        return self.collection.count()
    
    def clear_collection(self):
        """Clear all documents from collection"""
        self.client.delete_collection(Config.COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=Config.COLLECTION_NAME,
            metadata={"description": "Marmara University CENG Department documents"}
        )
