"""Tracing and logging components."""

from dataclasses import dataclass, asdict
from typing import Any
import time


@dataclass
class TraceEvent:
    """Represents a trace event from a pipeline stage."""
    
    stage_name: str
    input_summary: str
    output_summary: str
    duration_ms: int
    timestamp: float = 0.0
    
    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = time.time()
    
    def to_dict(self) -> dict:
        """Convert event to dictionary."""
        return asdict(self)
