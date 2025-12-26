
import unittest
from rag.reranker.reranker import PhraseAwareReranker, JaccardReranker
from rag.orchestrator.context import Context
from rag.retriever.hit import Hit
from rag.model.chunk import Chunk

class TestRerankers(unittest.TestCase):
    def setUp(self):
        self.chunk1 = Chunk(id="1", doc_id="d1", start_offset=0, end_offset=10, text="hello world")
        self.chunk2 = Chunk(id="2", doc_id="d1", start_offset=11, end_offset=20, text="hello universe")
        self.hits = [
            Hit(chunk=self.chunk1, initial_score=1.0),
            Hit(chunk=self.chunk2, initial_score=0.9)
        ]
        
    def test_phrase_aware_reranker(self):
        reranker = PhraseAwareReranker()
        context = Context(original_question="hello world")
        context.retrieval_hits = self.hits
        
        reranker.execute(context)
        
        # chunk1 should be boosted because it contains "hello world"
        self.assertTrue(context.retrieval_hits[0].rerank_score > context.retrieval_hits[1].rerank_score)
        self.assertEqual(context.retrieval_hits[0].chunk.id, "1")
        
    def test_jaccard_reranker(self):
        reranker = JaccardReranker()
        context = Context(original_question="hello world")
        context.retrieval_hits = self.hits
        
        reranker.execute(context)
        
        # chunk1: {hello, world} vs {hello, world} -> Jaccard 1.0
        # chunk2: {hello, universe} vs {hello, world} -> Jaccard 0.33
        
        self.assertTrue(context.retrieval_hits[0].rerank_score > context.retrieval_hits[1].rerank_score)
        self.assertEqual(context.retrieval_hits[0].chunk.id, "1")

    def test_reranker_empty(self):
        reranker = PhraseAwareReranker()
        context = Context(original_question="")
        reranker.execute(context)
        # Should not crash
        self.assertTrue(True)
