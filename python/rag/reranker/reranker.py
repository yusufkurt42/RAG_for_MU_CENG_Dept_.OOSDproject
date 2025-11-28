"""Reranking components."""

from typing import Protocol
from ..orchestrator.context import Context


class Reranker(Protocol):
    """Protocol for reranking strategies."""
    
    def execute(self, context: Context) -> None:
        """Execute reranking."""
        ...
    
    def get_name(self) -> str:
        """Get reranker name."""
        ...


class PhraseAwareReranker:
    """Reranker that boosts exact phrase matches."""
    
    PHRASE_BOOST = 5.0
    
    def execute(self, context: Context) -> None:
        """Execute reranking on the context."""
        query = context.original_question
        hits = context.retrieval_hits
        
        if not query or not hits:
            return
        
        lower_query = query.lower().strip()
        
        # Re-score: boost if exact query phrase appears
        for hit in hits:
            if hit.chunk.text and lower_query in hit.chunk.text.lower():
                hit.rerank_score = hit.initial_score + self.PHRASE_BOOST
        
        # Re-sort by rerank score (descending)
        hits.sort(key=lambda h: h.get_effective_score(), reverse=True)
        
        context.retrieval_hits = hits
        print(f"   -> PhraseAwareReranker re-sorted {len(hits)} hits")
    
    def get_name(self) -> str:
        """Get reranker name."""
        return "PhraseAwareReranker"
