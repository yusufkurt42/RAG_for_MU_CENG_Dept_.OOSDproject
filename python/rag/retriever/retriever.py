"""Retrieval components."""

from __future__ import annotations
from typing import TYPE_CHECKING, Protocol, List, Dict

# 1. Move import here
if TYPE_CHECKING:
    from ..orchestrator.context import Context

from typing import Protocol, List, Dict
import os
import json

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
        #print(f"   -> Retriever found {len(retrieval_hits)} results (k={self.k})")


    
    def get_name(self) -> str:
        """Get retriever name."""
        return "SimpleRetriever"


class CacheRetriever(SimpleRetriever):
    """Retriever with caching capabilities."""
    def __init__(self, index: KeywordIndex, k: int = 10, cache_file: str = "resources/cache.json"):
        super().__init__(index, k)
        self.cache_file = cache_file
        # Load cache directly in the constructor
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.cache = {}
        else:
            self.cache = {}

    def execute(self, context: Context) -> None:
        """Execute retrieval with caching."""
        query_terms = context.query_terms
        if not query_terms:
            context.retrieval_hits = []
            return

        # Create a cache key based on the query terms
        cache_key = tuple(sorted(query_terms))
        cache_key_str = json.dumps(cache_key)
        
        if cache_key_str in self.cache:
            # Use cached results
            try:
                cached_hits = []
                for hit_data in self.cache[cache_key_str]:
                    # Reconstruct Chunk object
                    chunk_data = hit_data['chunk']
                    chunk = Chunk(
                        id=chunk_data['id'],
                        doc_id=chunk_data['docId'],
                        start_offset=chunk_data['startOffset'],
                        end_offset=chunk_data['endOffset'],
                        text=chunk_data['text']
                    )
                    # Reconstruct Hit object
                    hit = Hit(
                        chunk=chunk,
                        initial_score=hit_data['initial_score'],
                        rerank_score=hit_data.get('rerank_score', 0.0)
                    )
                    cached_hits.append(hit)
                
                context.retrieval_hits = cached_hits
                return
            except (KeyError, TypeError) as e:
                print(f"Cache corruption detected: {e}. Ignoring cache.")

        # Perform retrieval if not cached
        scores = {}
        for term in query_terms:
            if not term:
                continue
            for chunk, frequency in self.index.search(term).items():
                scores[chunk] = scores.get(chunk, 0) + frequency

        # Sort and select top-k results
        sorted_chunks = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        top_hits = [Hit(chunk, score) for chunk, score in sorted_chunks[:self.k]]

        # Cache the results
        try:
            serialized_hits = []
            for hit in top_hits:
                serialized_hits.append({
                    'chunk': hit.chunk.to_dict(),
                    'initial_score': hit.initial_score,
                    'rerank_score': hit.rerank_score
                })
            
            self.cache[cache_key_str] = serialized_hits
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Failed to write cache: {e}")

        # Update context
        context.retrieval_hits = top_hits

    def get_name(self) -> str:
        """Get retriever name."""
        return "CacheRetriever"
