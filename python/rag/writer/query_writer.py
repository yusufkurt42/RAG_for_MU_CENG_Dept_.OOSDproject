"""Query writing components."""

from typing import List, Dict, Protocol
from ..detector.intent_detector import Intent
from ..orchestrator.context import Context


class QueryWriter(Protocol):
    """Protocol for query writing strategies."""
    
    def execute(self, context: Context) -> None:
        """Execute query writing."""
        ...
    
    def get_name(self) -> str:
        """Get writer name."""
        ...


class HeuristicQueryWriter:
    """Heuristic-based query writer with stemming and boosting."""
    
    def __init__(self, 
                 stopwords: List[str], 
                 boosters: Dict[Intent, List[str]],
                 suffix_list: List[str],
                 max_terms: int):
        """
        Initialize query writer.
        
        Args:
            stopwords: Words to exclude from query
            boosters: Intent-specific boost terms
            suffix_list: Suffixes for stemming
            max_terms: Maximum number of query terms
        """
        self.stopwords = set(word.lower() for word in stopwords)
        self.boosters = boosters
        # Sort suffixes by length (longest first) for stemming
        self.suffix_list = sorted(suffix_list, key=len, reverse=True)
        self.max_terms = max_terms
    
    def _stem_word(self, word: str) -> str:
        """Apply simple suffix-based stemming."""
        is_core = True
        while is_core:
            is_core = False
            for suffix in self.suffix_list:
                if word.endswith(suffix):
                    word = word[:-len(suffix)]
                    is_core = True
                    break
        return word
    
    def execute(self, context: Context) -> None:
        """Execute query writing on the context."""
        question = context.original_question
        intent = context.current_intent
        
        if not question:
            context.query_terms = []
            return
        
        # Normalize and split
        import re
        normalized = question.lower()
        # Remove punctuation except Turkish characters
        normalized = re.sub(r'[^\wçÇğĞıİöÖşŞüÜ\s]', ' ', normalized)
        split_terms = normalized.split()
        
        # Stem and filter
        terms = []
        for term in split_terms:
            if not term:
                continue
            
            # Stem the term
            stemmed = self._stem_word(term)
            
            # Filter: not empty, not stopword, not duplicate, under max
            if (stemmed and 
                stemmed not in self.stopwords and 
                stemmed not in terms and 
                len(terms) < self.max_terms):
                terms.append(stemmed)
        
        # Add booster terms (with priority)
        if intent and intent in self.boosters:
            booster_terms = self.boosters[intent]
            for booster in booster_terms:
                # Remove if already in list
                if booster in terms:
                    terms.remove(booster)
                # Add at the beginning
                terms.insert(0, booster)
                # Trim if exceeded max
                if len(terms) > self.max_terms:
                    terms = terms[:self.max_terms]
        
        context.query_terms = terms
    
    def get_name(self) -> str:
        """Get writer name."""
        return "query_writer"
