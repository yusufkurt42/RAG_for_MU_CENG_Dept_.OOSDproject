"""Trace bus for event distribution (Observer pattern)."""

from typing import List
from .trace_event import TraceEvent
from .trace_sink import TraceSink


class TraceBus:
    """
    Trace bus that distributes events to registered sinks.
    Implements the Observer pattern.
    """
    
    def __init__(self):
        """Initialize trace bus."""
        self.observers: List[TraceSink] = []
    
    def register(self, sink: TraceSink) -> None:
        """Register a trace sink."""
        self.observers.append(sink)
    
    def trace(self, event: TraceEvent) -> None:
        """Send event to all registered sinks."""
        for sink in self.observers:
            sink.log(event)
    
    def close_all(self) -> None:
        """Close all registered sinks."""
        for sink in self.observers:
            sink.close()
