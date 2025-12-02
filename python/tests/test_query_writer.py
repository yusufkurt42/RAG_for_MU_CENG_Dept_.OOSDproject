"""Tests for HeuristicQueryWriter."""

import pytest
from rag.detector import Intent
from rag.writer import HeuristicQueryWriter
from rag.orchestrator import Context


class TestHeuristicQueryWriter:
    """Test cases for HeuristicQueryWriter."""
    
    def test_basic_query_writing(self):
        """Test basic query writing with stopwords."""
        stopwords = ["bir", "ve", "nedir"]
        boosters = {}
        suffix_list = ["ler", "lar"]
        max_terms = 10
        
        writer = HeuristicQueryWriter(stopwords, boosters, suffix_list, max_terms)
        context = Context("öğrenciler ve öğretmenler nedir?")
        context.current_intent = Intent.UNKNOWN
        
        writer.execute(context)
        
        # Should remove stopwords and stem
        assert "nedir" not in context.query_terms
        assert "ve" not in context.query_terms
    
    def test_stemming(self):
        """Test suffix-based stemming."""
        stopwords = []
        boosters = {}
        suffix_list = ["ler", "lar", "den", "dan"]
        max_terms = 10
        
        writer = HeuristicQueryWriter(stopwords, boosters, suffix_list, max_terms)
        context = Context("öğrencilerden")
        context.current_intent = Intent.UNKNOWN
        
        writer.execute(context)
        
        # Should stem to "öğrenci"
        assert any("öğrenci" in term for term in context.query_terms)
    
    def test_booster_terms(self):
        """Test booster terms for specific intent."""
        stopwords = []
        boosters = {
            Intent.STAFF_LOOKUP: ["staff", "danisman"]
        }
        suffix_list = []
        max_terms = 10
        
        writer = HeuristicQueryWriter(stopwords, boosters, suffix_list, max_terms)
        context = Context("kimdir?")
        context.current_intent = Intent.STAFF_LOOKUP
        
        writer.execute(context)
        
        # Should have booster terms at the beginning
        assert "staff" in context.query_terms
        assert "danisman" in context.query_terms
    
    def test_max_terms_limit(self):
        """Test maximum terms limit."""
        stopwords = []
        boosters = {}
        suffix_list = []
        max_terms = 3
        
        writer = HeuristicQueryWriter(stopwords, boosters, suffix_list, max_terms)
        context = Context("one two three four five six")
        context.current_intent = Intent.UNKNOWN
        
        writer.execute(context)
        
        # Should not exceed max_terms
        assert len(context.query_terms) <= max_terms
    
    def test_empty_question(self):
        """Test empty question."""
        stopwords = []
        boosters = {}
        suffix_list = []
        max_terms = 10
        
        writer = HeuristicQueryWriter(stopwords, boosters, suffix_list, max_terms)
        context = Context("")
        context.current_intent = Intent.UNKNOWN
        
        writer.execute(context)
        
        assert context.query_terms == []
    
    def test_duplicate_removal(self):
        """Test duplicate term removal."""
        stopwords = []
        boosters = {}
        suffix_list = []
        max_terms = 10
        
        writer = HeuristicQueryWriter(stopwords, boosters, suffix_list, max_terms)
        context = Context("test test test")
        context.current_intent = Intent.UNKNOWN
        
        writer.execute(context)
        
        # Should only have one "test"
        assert context.query_terms.count("test") == 1
