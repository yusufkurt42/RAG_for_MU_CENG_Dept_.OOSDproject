"""Context object for maintaining pipeline state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..detector.intent_detector import Intent

from ..answer.answer import Answer
from ..retriever.retriever import Hit


@dataclass
class Context:
    """
    Context object that flows through the pipeline.
    Maintains state across different stages.
    """
    
    # Input
    original_question: str
    
    # Intent Detection Stage
    current_intent: Optional[Intent] = None
    
    # Query Writing Stage
    query_terms: List[str] = field(default_factory=list)
    
    # Policy Stage
    policy_violation: Optional[str] = None
    
    # Retrieval Stage
    retrieval_hits: List[Hit] = field(default_factory=list)
    
    # Answer Stage
    final_answer: Optional[Answer] = None
    
    def __str__(self) -> str:
        """String representation of context."""
        return f"Context(question='{self.original_question[:50]}...', intent={self.current_intent})"
