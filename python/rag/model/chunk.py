"""Data models for the RAG system."""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json


@dataclass(frozen=True)
class Chunk:
    """Represents a text chunk from a document."""
    
    id: str
    doc_id: str
    start_offset: int
    end_offset: int
    text: str
    
    def to_dict(self) -> Dict:
        """Convert chunk to dictionary."""
        return {
            "id": self.id,
            "docId": self.doc_id,
            "startOffset": self.start_offset,
            "endOffset": self.end_offset,
            "text": self.text
        }
    
    def to_json(self) -> str:
        """Convert chunk to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Chunk':
        """Create Chunk from dictionary."""
        return cls(
            id=data.get("id", ""),
            doc_id=data.get("docId", ""),
            start_offset=data.get("startOffset", 0),
            end_offset=data.get("endOffset", 0),
            text=data.get("text", "")
        )


class ChunkStore:
    """Storage for chunks with fast lookup by ID."""
    
    def __init__(self, chunk_map: Dict[str, Chunk]):
        """Initialize chunk store with a chunk map."""
        self._chunk_map = dict(chunk_map)  # Create immutable copy
    
    def get_chunk(self, chunk_id: str) -> Optional[Chunk]:
        """Get chunk by ID."""
        return self._chunk_map.get(chunk_id)
    
    def get_all_chunks(self) -> List[Chunk]:
        """Get all chunks as a list."""
        return list(self._chunk_map.values())
    
    def __len__(self) -> int:
        """Return number of chunks in store."""
        return len(self._chunk_map)
