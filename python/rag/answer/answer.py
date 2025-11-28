"""Answer generation components."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Answer:
    """Represents a generated answer with citations."""
    
    text: str
    citations: List[str] = field(default_factory=list)
    
    def __str__(self) -> str:
        """String representation of answer."""
        return self.text
