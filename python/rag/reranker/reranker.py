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


class PhraseAwareReranker(Reranker):
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
        #print(f"   -> PhraseAwareReranker re-sorted {len(hits)} hits")
    
    def get_name(self) -> str:
        """Get reranker name."""
        return "PhraseAwareReranker"

class JaccardReranker(Reranker):
    """
    Reranker that uses Jaccard Similarity (Intersection over Union).
    [Strategy - Concrete Implementation]
    """
    
    def execute(self, context: Context) -> None:
        """
        Calculates Jaccard similarity between query and chunk text.
        Updates rerank_score and sorts hits.
        """
        query = context.original_question
        hits = context.retrieval_hits
        
        if not query or not hits:
            return
            
        # Pre-process query into a set of unique words
        query_tokens = set(query.lower().split())
        
        if not query_tokens:
            return

        for hit in hits:
            if not hit.chunk.text:
                continue
                
            # Pre-process chunk text into a set
            chunk_tokens = set(hit.chunk.text.lower().split())
            
            # Calculate Jaccard Index
            intersection = query_tokens.intersection(chunk_tokens)
            union = query_tokens.union(chunk_tokens)
            
            jaccard_score = 0.0
            if len(union) > 0:
                jaccard_score = len(intersection) / len(union)
            
            # Update score (Combine initial retrieval score with Jaccard score)
            # We treat Jaccard (0.0 to 1.0) as a boost to the initial score.
            # You might want to weigh this (e.g., * 10) depending on your initial score scale.
            hit.rerank_score = hit.initial_score + (jaccard_score * 5.0) 

        # Re-sort by effective score (descending)
        hits.sort(key=lambda h: h.get_effective_score(), reverse=True)
        
        context.retrieval_hits = hits
        #print(f"   -> JaccardReranker re-sorted {len(hits)} hits")

    def get_name(self) -> str:
        return "JaccardReranker"