"""Tests for RuleIntentDetector."""

import pytest
from rag.detector import Intent, RuleIntentDetector
from rag.orchestrator import Context


class TestRuleIntentDetector:
    """Test cases for RuleIntentDetector."""
    
    def test_single_match(self):
        """Test single intent match."""
        rules = {
            Intent.REGISTRATION: ["kayit", "yazilma"],
            Intent.STAFF_LOOKUP: ["danışman", "ofis"],
        }
        priority = [1, 0]
        
        detector = RuleIntentDetector(rules, priority)
        context = Context("danışman kimdir?")
        
        detector.execute(context)
        
        assert context.current_intent == Intent.STAFF_LOOKUP
    
    def test_no_match(self):
        """Test no intent match."""
        rules = {
            Intent.REGISTRATION: ["kayit", "yazilma"],
        }
        priority = []
        
        detector = RuleIntentDetector(rules, priority)
        context = Context("random question")
        
        detector.execute(context)
        
        assert context.current_intent == Intent.UNKNOWN
    
    def test_multiple_matches_with_priority(self):
        """Test multiple matches resolved by priority."""
        rules = {
            Intent.REGISTRATION: ["kayit", "tarihleri"],
            Intent.STAFF_LOOKUP: ["danışman", "tarihleri"],
        }
        priority = [1, 0]  # STAFF_LOOKUP has higher priority
        
        detector = RuleIntentDetector(rules, priority)
        context = Context("tarihleri nedir?")
        
        detector.execute(context)
        
        # Should match STAFF_LOOKUP due to priority
        assert context.current_intent == Intent.STAFF_LOOKUP
    
    def test_empty_question(self):
        """Test empty question."""
        rules = {Intent.REGISTRATION: ["kayit"]}
        priority = []
        
        detector = RuleIntentDetector(rules, priority)
        context = Context("")
        
        detector.execute(context)
        
        assert context.current_intent == Intent.UNKNOWN
    
    def test_case_insensitive(self):
        """Test case insensitive matching."""
        rules = {
            Intent.REGISTRATION: ["kayit"],
        }
        priority = []
        
        detector = RuleIntentDetector(rules, priority)
        context = Context("KAYIT nedir?")
        
        detector.execute(context)
        
        assert context.current_intent == Intent.REGISTRATION
