"""Utility functions for loading data."""

from typing import Dict, Any
import json
from ..model import ChunkStore
from ..store.json_chunk_store import JsonChunkStore


class ChunkStoreLoader:
    """Utility for loading chunk stores."""
    
    @staticmethod
    def load(chunk_path: str) -> ChunkStore:
        """
        Load chunk store from file.
        
        Args:
            chunk_path: Path to chunk file
            
        Returns:
            ChunkStore instance
        """
        return JsonChunkStore.load(chunk_path)


class JsonConfigLoader:
    """Utility for loading JSON configuration files."""
    
    @staticmethod
    def load_and_parse(config_path: str) -> Dict[str, Any]:
        """
        Load and parse JSON configuration file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Dictionary of configuration data
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
