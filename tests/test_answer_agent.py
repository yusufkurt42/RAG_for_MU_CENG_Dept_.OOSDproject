
import unittest
from rag.answer.answer_agent import TemplateAnswerAgent
from rag.orchestrator.context import Context
from rag.retriever.hit import Hit
from rag.model.chunk import Chunk
from rag.model.chunk import Chunk
from unittest.mock import MagicMock

class TestTemplateAnswerAgent(unittest.TestCase):
    def setUp(self):
        self.store = MagicMock()
        self.agent = TemplateAnswerAgent(self.store)
        
    def test_policy_violation(self):
        context = Context(original_question="bad question")
        context.policy_violation = "Illegal content"
        self.agent.execute(context)
        
        self.assertIn("reddedildi", context.final_answer.text)
        
    def test_no_hits(self):
        context = Context(original_question="question")
        context.retrieval_hits = []
        self.agent.execute(context)
        
        self.assertIn("bulunamadı", context.final_answer.text)
        
    def test_generate_answer(self):
        chunk = Chunk(id="1", doc_id="d1", start_offset=0, end_offset=10, text="The answer is 42. Another sentence.")
        hit = Hit(chunk=chunk, initial_score=1.0)
        context = Context(original_question="what is answer")
        context.query_terms = ["answer"]
        context.retrieval_hits = [hit]
        
        self.agent.execute(context)
        
        # Should pick the sentence with "answer"
        self.assertIn("The answer is 42", context.final_answer.text)
