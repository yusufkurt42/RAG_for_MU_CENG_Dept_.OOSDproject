import re
from typing import List, Dict
from src.rag.orchestrator.context import Context
from src.rag.retriever.base import Retriever
from src.rag.retriever.index import KeywordIndex
from src.rag.retriever.hit import Hit
from src.rag.model.chunk import Chunk

class SimpleRetriever(Retriever):
    """
    Implementation of keyword-based retrieval.
    """
    def __init__(self, index: KeywordIndex, k: int):
        self._index = index
        self._k = k

    def execute(self, context: Context) -> None:
        query = context.original_question
        if not query: return

        # Query parsing
        query_terms = [t for t in re.split(r'\W+', query.lower()) if t]
        if not context.query_terms:
            context.query_terms = query_terms

        # TF Scoring Logic
        scores: Dict[Chunk, float] = {}
        for term in query_terms:
            matches = self._index.search(term)
            for chunk, tf in matches.items():
                scores[chunk] = scores.get(chunk, 0.0) + tf

        # Sorting and Top-K Selection
        sorted_items = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        top_k = sorted_items[:self._k]

        # Convert to Hits
        hits = [Hit(chunk, score) for chunk, score in top_k]

        # Update Context
        context.set_retrieval_hits(hits)
        print(f"[{self.get_name()}] Found {len(hits)} results.")

    def get_name(self) -> str:
        return "SimpleRetriever"