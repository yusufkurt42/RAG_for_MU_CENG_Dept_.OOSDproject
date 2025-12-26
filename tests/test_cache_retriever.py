
import unittest
import json
import os
import shutil
from rag.retriever.retriever import CacheRetriever
from rag.retriever.keyword_index import KeywordIndex
from rag.model.chunk import Chunk
from rag.orchestrator.context import Context

class TestCacheRetriever(unittest.TestCase):
    def setUp(self):
        self.test_cache_file = "tests/test_cache.json"
        if os.path.exists(self.test_cache_file):
            os.remove(self.test_cache_file)
            
        # Create dummy chunks
        self.chunks = [
            Chunk(id="1", doc_id="doc1", start_offset=0, end_offset=10, text="apple banana"),
            Chunk(id="2", doc_id="doc1", start_offset=11, end_offset=20, text="banana cherry"),
            Chunk(id="3", doc_id="doc2", start_offset=0, end_offset=10, text="apple cherry date")
        ]
        
        # Create index
        self.index = KeywordIndex()
        self.index.build_from_chunks(self.chunks)
        
    def tearDown(self):
        if os.path.exists(self.test_cache_file):
            os.remove(self.test_cache_file)

    def test_caching_mechanism(self):
        retriever = CacheRetriever(self.index, k=2, cache_file=self.test_cache_file)
        
        # First query - should be a miss and write to cache
        context1 = Context(original_question="apple")
        context1.query_terms = ["apple"]
        
        retriever.execute(context1)
        
        self.assertTrue(len(context1.retrieval_hits) > 0)
        self.assertTrue(os.path.exists(self.test_cache_file))
        
        # Verify cache content
        with open(self.test_cache_file, 'r') as f:
            cache_data = json.load(f)
            key = json.dumps(["apple"])
            self.assertIn(key, cache_data)
            
        # Second query - should be a hit
        # Create a new retriever instance to simulate a fresh run, but pointing to same cache file
        retriever2 = CacheRetriever(self.index, k=2, cache_file=self.test_cache_file)
        
        context2 = Context(original_question="apple")
        context2.query_terms = ["apple"]
        
        # Modify the index of retriever2 to ensure it's not using the index (optional, but good for verification)
        # But CacheRetriever uses cache if key exists.
        
        retriever2.execute(context2)
        
        self.assertEqual(len(context2.retrieval_hits), len(context1.retrieval_hits))
        self.assertEqual(context2.retrieval_hits[0].chunk.id, context1.retrieval_hits[0].chunk.id)
        
        # Verify that the hits in context2 are proper objects
        self.assertIsInstance(context2.retrieval_hits[0].chunk, Chunk)

if __name__ == '__main__':
    unittest.main()
