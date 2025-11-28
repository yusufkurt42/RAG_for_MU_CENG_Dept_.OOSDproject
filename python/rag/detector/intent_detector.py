"""Intent detection components."""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from ..orchestrator.context import Context


class Intent(Enum):
    """Intent types for user queries."""
    STAFF_LOOKUP = 0
    REGISTRATION = 1
    POLICY_FAQ = 2
    COURSE = 3
    UNKNOWN = 4



class IntentDetector(Protocol):
    """Interface for intent detection strategies."""

    def execute(self, context: "Context") -> None:
        """Execute intent detection and update context."""
        ...

    def get_name(self) -> str:
        """Get detector name."""
        ...


class RuleIntentDetector:
    """Rule-based intent detector using keyword matching."""
    
    def __init__(self, intent_rules: Dict[Intent, List[str]], priority: List[int]):
        """
        Initialize rule detector.
        
        Args:
            intent_rules: Map of Intent to keyword lists
            priority: Priority order of intents (by ordinal value)
        """
        self.intent_rules = intent_rules if intent_rules else {}
        self.priority = priority if priority else []
    
    def execute(self, context: Context) -> None:
        """Execute intent detection on the context."""
        question = context.original_question
        
        if not question or not question.strip():
            context.current_intent = Intent.UNKNOWN
            return
        
        # Normalize question
        normalized_question = question.lower()
        
        # Find matching intents
        candidates = []
        for intent, keywords in self.intent_rules.items():
            for keyword in keywords:
                if keyword.lower() in normalized_question:
                    candidates.append(intent)
                    break
        
        # No candidates found
        if not candidates:
            context.current_intent = Intent.UNKNOWN
            return
        
        # Single candidate
        if len(candidates) == 1:
            context.current_intent = candidates[0]
            return
        
        # Multiple candidates - use priority
        if self.priority:
            for intent_ordinal in self.priority:
                if 0 <= intent_ordinal < len(Intent):
                    priority_intent = list(Intent)[intent_ordinal]
                    if priority_intent in candidates:
                        context.current_intent = priority_intent
                        return
        
        # Default to first candidate
        context.current_intent = candidates[0]
    
    def get_name(self) -> str:
        """Get detector name."""
        return "intent_detector"
