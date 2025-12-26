"""Ollama LLM Client."""

from typing import Optional
from ollamafreeapi import OllamaFreeAPI

class OllamaLLM:
    """Client for Ollama LLM using free cloud API."""
    
    def __init__(self, base_url: str = "", model_name: str = "llama3"):
        """
        Initialize Ollama client.
        
        Args:
            base_url: Ignored for free API (kept for compatibility)
            model_name: Model name (default: llama3)
        """
        self.client = OllamaFreeAPI()
        self.model_name = model_name
        
    def generate_content(self, prompt: str) -> str:
        """
        Generate content from prompt.
        
        Args:
            prompt: Input text
            
        Returns:
            Generated text response
        """
        try:
            return self.client.chat(prompt=prompt, model=self.model_name)
        except Exception as e:
            return f"Error generating response: {str(e)}"
