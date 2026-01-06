
import unittest
from rag.detector.intent_detector import RuleIntentDetector, Intent
from rag.orchestrator.context import Context

class TestRuleIntentDetector(unittest.TestCase):
    def setUp(self):
        self.rules = {
            Intent.STAFF_LOOKUP: ["staff", "professor"],
            Intent.REGISTRATION: ["register", "enroll"]
        }
        self.priority = [0, 1] # STAFF_LOOKUP, REGISTRATION
        self.detector = RuleIntentDetector(self.rules, self.priority)
        
    def test_detect_staff(self):
        context = Context(original_question="Where is the staff office?")
        self.detector.execute(context)
        self.assertEqual(context.current_intent, Intent.STAFF_LOOKUP)
        
    def test_detect_unknown(self):
        context = Context(original_question="What is the weather?")
        self.detector.execute(context)
        self.assertEqual(context.current_intent, Intent.UNKNOWN)
        
    def test_empty_question(self):
        context = Context(original_question="")
        self.detector.execute(context)
        self.assertEqual(context.current_intent, Intent.UNKNOWN)
        
    def test_priority_resolution(self):
        # Both keywords present
        context = Context(original_question="staff register")
        self.detector.execute(context)
        # Should pick STAFF_LOOKUP based on priority list [0, 1]
        self.assertEqual(context.current_intent, Intent.STAFF_LOOKUP)

    def test_get_name(self):
        self.assertEqual(self.detector.get_name(), "intent_detector")
