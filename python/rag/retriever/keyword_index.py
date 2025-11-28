"""Keyword index for retrieval."""

from typing import Dict, List
from collections import defaultdict
from ..model import Chunk


class KeywordIndex:
    """Inverted index for keyword-based retrieval."""
    
    def __init__(self):
        """Initialize empty index."""
        # Maps term -> {chunk -> term_frequency}
        self.index: Dict[str, Dict[Chunk, int]] = defaultdict(lambda: defaultdict(int))
    
    def add_chunk(self, chunk: Chunk) -> None:
        """Add a chunk to the index."""
        if not chunk.text:
            return
        
        # Tokenize chunk text
        terms = chunk.text.lower().split()
        
        # Count term frequencies
        for term in terms:
            if term:  # Skip empty terms
                self.index[term][chunk] += 1
    
    def search(self, term: str) -> Dict[Chunk, int]:
        """
        Search for chunks containing the term.
        
        Args:
            term: Search term
            
        Returns:
            Dictionary of chunks with term frequencies
        """
        return dict(self.index.get(term.lower(), {}))
    
    def build_from_chunks(self, chunks: List[Chunk]) -> None:
        """Build index from a list of chunks."""
        for chunk in chunks:
            self.add_chunk(chunk)
    
    @classmethod
    def load_from_dict(cls, data: Dict) -> 'KeywordIndex':
        """
        Load index from dictionary.
        
        Note: This requires chunks to be reconstructed.
        For simplicity, we'll rebuild from chunk store.
        """
        index = cls()
        # Index data would need special serialization
        # For now, return empty index
        return index
