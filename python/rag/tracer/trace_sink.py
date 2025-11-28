"""Trace sink interface and implementations."""

from abc import ABC, abstractmethod
from typing import IO
import json
import os
from datetime import datetime
from .trace_event import TraceEvent


class TraceSink(ABC):
    """Abstract base class for trace sinks."""
    
    @abstractmethod
    def log(self, event: TraceEvent) -> None:
        """Log a trace event."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close the sink and flush any buffered data."""
        pass


class JsonlTraceSink(TraceSink):
    """JSONL (JSON Lines) trace sink that writes to a file."""
    
    def __init__(self, log_dir: str = "logs"):
        """
        Initialize JSONL trace sink.
        
        Args:
            log_dir: Directory to write log files
        """
        self.log_dir = log_dir
        self.file_handle: IO | None = None
        self._ensure_log_dir()
        self._open_log_file()
    
    def _ensure_log_dir(self) -> None:
        """Create log directory if it doesn't exist."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _open_log_file(self) -> None:
        """Open a new log file with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"run-{timestamp}.jsonl"
        filepath = os.path.join(self.log_dir, filename)
        self.file_handle = open(filepath, 'w', encoding='utf-8')
    
    def log(self, event: TraceEvent) -> None:
        """Log an event as a JSON line."""
        if self.file_handle:
            json_line = json.dumps(event.to_dict())
            self.file_handle.write(json_line + '\n')
            self.file_handle.flush()
    
    def close(self) -> None:
        """Close the log file."""
        if self.file_handle:
            self.file_handle.close()
            self.file_handle = None
