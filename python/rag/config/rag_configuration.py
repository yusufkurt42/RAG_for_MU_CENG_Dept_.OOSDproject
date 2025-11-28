"""Configuration management for RAG system."""

from dataclasses import dataclass
from typing import Dict, List, Any
import json


@dataclass
class RagConfiguration:
    """Configuration for RAG system."""
    
    window_size: int = 400
    overlap: int = 50
    input_file_path: str = "Bilimsel_Etkinlik_Katilimi_Dilekce.pdf"
    output_file_path: str = "data/chunks.json"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RagConfiguration':
        """Create configuration from dictionary."""
        return cls(
            window_size=data.get("windowSize", 400),
            overlap=data.get("overlap", 50),
            input_file_path=data.get("inputFilePath", ""),
            output_file_path=data.get("outputFilePath", "")
        )


class JsonConfigLoader:
    """Loads and parses JSON configuration files."""
    
    @staticmethod
    def load_and_parse(config_path: str) -> Dict[str, Any]:
        """Load and parse JSON configuration file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file: {e}")
