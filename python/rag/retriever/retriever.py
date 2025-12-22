"""Retrieval components."""

from __future__ import annotations
from typing import TYPE_CHECKING, Protocol, List

# 1. Move import here
if TYPE_CHECKING:
    from ..orchestrator.context import Context

from ..model import Chunk
from .keyword_index import KeywordIndex
from .hit import Hit


class Retriever(Protocol):
    """Protocol for retrieval strategies."""
    
    def execute(self, context: Context) -> None:
        """Execute retrieval."""
        ...
    
    def get_name(self) -> str:
        """Get retriever name."""
        ...

class SimpleRetriever:
    """Simple keyword-based retriever."""
    
    def __init__(self, index: KeywordIndex, k: int = 10):
        """
        Initialize retriever.
        
        Args:
            index: Keyword index to use
            k: Number of top results to return
        """
        self.index = index
        self.k = k
    
    def execute(self, context: Context) -> None:
        """Execute retrieval on the context."""
        query_terms = context.query_terms
        
        if not query_terms:
            context.retrieval_hits = []
            return
        
        # Score chunks by keyword matching
        scores: Dict[Chunk, float] = {}
        
        for term in query_terms:
            if not term:
                continue
            
            # Find chunks from index
            matches = self.index.search(term)
            
            for chunk, tf in matches.items():
                scores[chunk] = scores.get(chunk, 0.0) + tf
        
        # Sort by score (descending)
        sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Take top K
        top_items = sorted_items[:self.k]
        
        # Convert to Hit objects
        retrieval_hits = [
            Hit(chunk=chunk, initial_score=score)
            for chunk, score in top_items
        ]
        
        context.retrieval_hits = retrieval_hits
        print(f"   -> Retriever found {len(retrieval_hits)} results (k={self.k})")


    
    def get_name(self) -> str:
        """Get retriever name."""
        return "SimpleRetriever"
