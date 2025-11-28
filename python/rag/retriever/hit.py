"""Retrieval components."""

from dataclasses import dataclass
from ..model import Chunk


@dataclass
class Hit:
    """Represents a retrieval hit with score."""
    
    chunk: Chunk
    initial_score: float
    rerank_score: float = 0.0
    
    def __post_init__(self):
        """Initialize rerank score to initial score if not set."""
        if self.rerank_score is None:
            self.rerank_score = self.initial_score
    
    def get_effective_score(self) -> float:
        """Get the effective score (rerank if available, otherwise initial)."""
        return self.rerank_score if self.rerank_score is not None else self.initial_score
