"""Policy enforcement components."""

from typing import List, Protocol
from ..orchestrator.context import Context


class PolicyRerouter(Protocol):
    """Protocol for policy enforcement strategies."""
    
    def execute(self, context: Context) -> None:
        """Execute policy check."""
        ...
    
    def get_name(self) -> str:
        """Get component name."""
        ...


class KeywordPolicyRerouter:
    """Policy rerouter that rejects queries containing banned keywords."""
    
    def __init__(self, banned_keywords: List[str]):
        """
        Initialize policy rerouter.
        
        Args:
            banned_keywords: List of keywords that are not allowed
        """
        self.banned_keywords = [k.lower() for k in banned_keywords]
    
    def execute(self, context: Context) -> None:
        """
        Check if query terms contain banned keywords.
        If banned keyword found, clear query terms to stop processing.
        """
        if not context.query_terms:
            return
            
        # Check against processed query terms
        for term in context.query_terms:
            term_lower = term.lower()
            if term_lower in self.banned_keywords:
                # Policy violation found
                # Clear query terms to prevent retrieval
                context.query_terms = []
                context.policy_violation = f"Query contains banned keyword: '{term}'"
                # Set a special flag or intent if needed, or just let it fail gracefully
                # For now, we'll just print a message (in a real system, we might set an error state)
                print(f"   -> Policy violation: banned keyword '{term}' found")
                return
    
    def get_name(self) -> str:
        """Get component name."""
        return "KeywordPolicyRerouter"
