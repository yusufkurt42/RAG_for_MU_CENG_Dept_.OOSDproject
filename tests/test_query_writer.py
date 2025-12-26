
import unittest
from rag.writer.query_writer import HeuristicQueryWriter
from rag.detector.intent_detector import Intent
from rag.orchestrator.context import Context

class TestHeuristicQueryWriter(unittest.TestCase):
    def setUp(self):
        self.stopwords = ["is", "the", "a"]
        self.boosters = {Intent.STAFF_LOOKUP: ["office"]}
        self.suffix_list = ["ing", "s"]
        self.writer = HeuristicQueryWriter(self.stopwords, self.boosters, self.suffix_list, max_terms=5)
        
    def test_basic_writing(self):
        context = Context(original_question="Where is the testing office")
        context.current_intent = Intent.STAFF_LOOKUP
        self.writer.execute(context)
        
        # "Where" -> "where" (not stopword)
        # "is" -> stopword
        # "the" -> stopword
        # "testing" -> "test" (suffix "ing")
        # "office" -> "office"
        # Booster "office" added to front
        
        self.assertIn("test", context.query_terms)
        self.assertIn("office", context.query_terms)
        self.assertEqual(context.query_terms[0], "office") # Booster first
        
    def test_empty_question(self):
        context = Context(original_question="")
        self.writer.execute(context)
        self.assertEqual(context.query_terms, [])
        
    def test_max_terms(self):
        writer = HeuristicQueryWriter([], {}, [], max_terms=2)
        context = Context(original_question="one two three")
        writer.execute(context)
        self.assertEqual(len(context.query_terms), 2)

    def test_stemming(self):
        # "testing" -> "test"
        self.assertEqual(self.writer._stem_word("testing"), "test")
        # "cats" -> "cat"
        self.assertEqual(self.writer._stem_word("cats"), "cat")
