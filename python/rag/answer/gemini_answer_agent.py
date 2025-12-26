"""Gemini-based answer agent."""

from typing import List
from ..orchestrator.context import Context
from ..llm.gemini_llm import GeminiLLM
from .answer import Answer

class GeminiAnswerAgent:
    """Answer agent that uses Gemini LLM."""
    
    def __init__(self, llm: GeminiLLM):
        """
        Initialize agent.
        
        Args:
            llm: Configured Gemini LLM client
        """
        self.llm = llm
        
    def execute(self, context: Context) -> None:
        """Execute answer generation."""
        query = " ".join(context.query_terms) if context.query_terms else ""
        
        # Format context from hits
        context_text = ""
        if context.retrieval_hits:
            for i, hit in enumerate(context.retrieval_hits):
                context_text += f"\nSource {i+1}:\n{hit.chunk.text}\n"
        
        # Construct prompt
        prompt = self._construct_prompt(query, context_text)
        
        # Generate answer
        response_text = self.llm.generate_content(prompt)
        
        # Create Answer object
        context.final_answer = Answer(
            text=response_text,
            citations=[hit.chunk.doc_id for hit in context.retrieval_hits]
        )
        
    def _construct_prompt(self, query: str, context_text: str) -> str:
        """Construct the prompt for Gemini."""
        return f"""You are a helpful assistant for a university. 
Use the following context to answer the user's question.
If the answer is not in the context, say you don't know.

Context:
{context_text}

Question: {query}

Answer:"""

    def get_name(self) -> str:
        return "GeminiAnswerAgent"
