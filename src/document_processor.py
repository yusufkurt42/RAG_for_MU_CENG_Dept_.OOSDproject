"""
Document processor for handling and chunking documents
"""
from typing import List, Dict
import os

class DocumentProcessor:
    """Process and chunk documents for RAG system"""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """
        Initialize document processor
        
        Args:
            chunk_size: Size of each text chunk
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def load_documents_from_directory(self, directory: str) -> List[Dict[str, str]]:
        """
        Load documents from a directory
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            List of document dictionaries with content and metadata
        """
        documents = []
        
        if not os.path.exists(directory):
            return documents
        
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    documents.append({
                        'content': content,
                        'source': filename,
                        'metadata': {'filename': filename}
                    })
        
        return documents
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundaries
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > 0:
                    chunk = text[start:start + break_point + 1]
                    end = start + break_point + 1
            
            chunks.append(chunk.strip())
            start = end - self.chunk_overlap
        
        return [chunk for chunk in chunks if chunk]
    
    def process_documents(self, documents: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Process documents by chunking them
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of chunked documents with metadata
        """
        processed_docs = []
        
        for doc in documents:
            chunks = self.chunk_text(doc['content'])
            for i, chunk in enumerate(chunks):
                processed_docs.append({
                    'content': chunk,
                    'source': doc['source'],
                    'chunk_id': i,
                    'metadata': doc.get('metadata', {})
                })
        
        return processed_docs
