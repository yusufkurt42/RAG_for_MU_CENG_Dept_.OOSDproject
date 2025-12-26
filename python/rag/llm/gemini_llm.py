"""Gemini LLM Client."""

import os
import google.generativeai as genai
from typing import Optional

class GeminiLLM:
    """Client for Google's Gemini LLM."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-pro"):
        """
        Initialize Gemini client.
        
        Args:
            api_key: Google API Key
            model_name: Model name (default: gemini-pro)
        """
        genai.configure(api_key=os.environ['GEMINI_API_KEY'])
        self.model = genai.GenerativeModel(model_name)
        
    def generate_content(self, prompt: str) -> str:
        """
        Generate content from prompt.
        
        Args:
            prompt: Input text
            
        Returns:
            Generated text response
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
