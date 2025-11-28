"""JSON-based chunk store."""

import json
from typing import Dict
from ..model import Chunk, ChunkStore


class JsonChunkStore:
    """Utility for loading chunks from JSON files."""
    
    @staticmethod
    def load(file_path: str) -> ChunkStore:
        """
        Load chunks from JSON file.
        
        Args:
            file_path: Path to JSON file containing chunks
            
        Returns:
            ChunkStore with loaded chunks
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Build chunk map
            chunk_map: Dict[str, Chunk] = {}
            
            # Handle different JSON structures
            if isinstance(data, list):
                # Array of chunks
                for item in data:
                    chunk = Chunk.from_dict(item)
                    chunk_map[chunk.id] = chunk
            elif isinstance(data, dict):
                # Object with chunk IDs as keys
                for chunk_id, item in data.items():
                    if isinstance(item, dict):
                        chunk = Chunk.from_dict(item)
                        chunk_map[chunk.id] = chunk
            
            return ChunkStore(chunk_map)
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Chunk file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in chunk file: {e}")
