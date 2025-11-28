"""Text chunking implementations."""

from abc import ABC, abstractmethod
from typing import List
from ..model import Chunk


class IChunker(ABC):
    """Interface for text chunking strategies."""
    
    @abstractmethod
    def chunk(self, doc_id: str, full_text: str) -> List[Chunk]:
        """
        Chunk the given text into segments.
        
        Args:
            doc_id: Document identifier
            full_text: Full text to chunk
            
        Returns:
            List of Chunk objects
        """
        pass


class SlidingWindowChunker(IChunker):
    """Sliding window chunker with overlap."""
    
    def __init__(self, window_size: int, overlap: int):
        """
        Initialize chunker.
        
        Args:
            window_size: Size of each chunk
            overlap: Overlap between consecutive chunks
            
        Raises:
            ValueError: If overlap >= window_size
        """
        if overlap >= window_size:
            raise ValueError("Overlap cannot be greater than or equal to window_size")
        
        self.window_size = window_size
        self.overlap = overlap
    
    def chunk(self, doc_id: str, full_text: str) -> List[Chunk]:
        """Chunk text using sliding window approach."""
        chunks = []
        
        if not full_text:
            return chunks
        
        text_length = len(full_text)
        start = 0
        
        while start < text_length:
            end = min(start + self.window_size, text_length)
            chunk_text = full_text[start:end]
            
            # Normalize text
            normalized_text = chunk_text.lower().strip()
            
            # Create chunk ID
            chunk_id = f"{doc_id}_{len(chunks) + 1}"
            
            chunks.append(Chunk(
                id=chunk_id,
                doc_id=doc_id,
                start_offset=start,
                end_offset=end,
                text=normalized_text
            ))
            
            if end == text_length:
                break
            
            start += (self.window_size - self.overlap)
        
        return chunks
