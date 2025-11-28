"""Answer generation components."""

from __future__ import annotations

from typing import List, Protocol
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # This runs only during type checking, not at runtime
    from ..orchestrator.context import Context
    
from ..model import ChunkStore
from .answer import Answer


class AnswerAgent(Protocol):
    """Protocol for answer generation strategies."""
    
    def execute(self, context: Context) -> None:
        """Execute answer generation."""
        ...
    
    def get_name(self) -> str:
        """Get agent name."""
        ...


class TemplateAnswerAgent:
    """Template-based answer agent."""
    
    def __init__(self, store: ChunkStore):
        """
        Initialize answer agent.
        
        Args:
            store: Chunk store for fetching chunks
        """
        self.store = store
    
    def execute(self, context: Context) -> None:
        """Execute answer generation on the context."""
        query_terms = context.query_terms
        top_hits = context.retrieval_hits
        
        answer = self._generate_answer(query_terms, top_hits)
        context.final_answer = answer
    
    def _generate_answer(self, query: List[str], top_hits: List) -> Answer:
        """Generate answer from query and hits."""
        # No hits case
        if not top_hits:
            return Answer(
                text="Üzgünüz, sorunuzla ilgili yeterli bilgi bulunamadı.",
                citations=[]
            )
        
        # Get best hit
        best_hit = top_hits[0]
        best_chunk = best_hit.chunk
        
        if not best_chunk:
            return Answer(
                text="Kaynak metin bulunamadı, indeks hatası.",
                citations=[]
            )
        
        # Split into sentences
        chunk_content = best_chunk.text
        sentences = re.split(r'[.?!]', chunk_content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return Answer(
                text="Metin içeriği bulunamadı.",
                citations=[]
            )
        
        # Find sentence with most query term matches
        best_sentence = sentences[0]
        max_matches = 0
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            matches = sum(1 for term in query if term in sentence_lower)
            if matches > max_matches:
                max_matches = matches
                best_sentence = sentence
        
        # Create citation
        citation = (f"{best_chunk.doc_id}:{best_chunk.id}:"
                   f"{best_chunk.start_offset}-{best_chunk.end_offset}")
        
        # Create final answer
        final_text = f"Your answer: {best_sentence}. See: {citation}"
        
        return Answer(text=final_text, citations=[citation])
    
    def get_name(self) -> str:
        """Get agent name."""
        return "answer_agent"
