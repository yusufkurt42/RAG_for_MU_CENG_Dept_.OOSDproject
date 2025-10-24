"""
Gemini API integration for text generation
"""
import google.generativeai as genai
from typing import List, Dict
from src.config import Config

class GeminiGenerator:
    """Generate responses using Gemini API"""
    
    def __init__(self):
        """Initialize Gemini generator"""
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def generate_response(self, query: str, context_documents: List[Dict[str, str]]) -> str:
        """
        Generate response using query and retrieved context
        
        Args:
            query: User query
            context_documents: Retrieved relevant documents
            
        Returns:
            Generated response
        """
        # Build context from retrieved documents
        context = self._build_context(context_documents)
        
        # Create prompt
        prompt = self._create_prompt(query, context)
        
        try:
            # Generate response
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _build_context(self, documents: List[Dict[str, str]]) -> str:
        """
        Build context string from documents
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            Formatted context string
        """
        if not documents:
            return "No relevant context found."
        
        context_parts = []
        for i, doc in enumerate(documents, 1):
            source = doc.get('metadata', {}).get('source', 'Unknown')
            content = doc.get('content', '')
            context_parts.append(f"[Document {i} - Source: {source}]\n{content}")
        
        return "\n\n".join(context_parts)
    
    def _create_prompt(self, query: str, context: str) -> str:
        """
        Create prompt for Gemini
        
        Args:
            query: User query
            context: Retrieved context
            
        Returns:
            Formatted prompt
        """
        prompt = f"""You are an AI assistant specialized in answering questions about Marmara University's Computer Engineering Department.

Use the following context documents to answer the user's question. If the context doesn't contain enough information to answer the question, say so and provide what information you can.

Context:
{context}

User Question: {query}

Please provide a comprehensive and accurate answer based on the context provided. If you use information from the context, mention which document it came from."""
        
        return prompt
