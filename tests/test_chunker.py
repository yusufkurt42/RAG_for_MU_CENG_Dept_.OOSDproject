
import unittest
from rag.chunker.chunker import SlidingWindowChunker
from rag.model.chunk import Chunk

class TestSlidingWindowChunker(unittest.TestCase):
    def test_chunking_basic(self):
        chunker = SlidingWindowChunker(window_size=10, overlap=2)
        text = "abcdefghijklmnopqrstuvwxyz"
        chunks = chunker.chunk("doc1", text)
        
        self.assertTrue(len(chunks) > 0)
        self.assertEqual(chunks[0].text, "abcdefghij")
        self.assertEqual(chunks[1].text, "ijklmnopqr")
        
    def test_chunking_empty(self):
        chunker = SlidingWindowChunker(window_size=10, overlap=2)
        chunks = chunker.chunk("doc1", "")
        self.assertEqual(len(chunks), 0)
        
    def test_invalid_overlap(self):
        with self.assertRaises(ValueError):
            SlidingWindowChunker(window_size=10, overlap=10)
            
    def test_chunk_attributes(self):
        chunker = SlidingWindowChunker(window_size=5, overlap=0)
        text = "hello"
        chunks = chunker.chunk("doc1", text)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].doc_id, "doc1")
        self.assertEqual(chunks[0].start_offset, 0)
        self.assertEqual(chunks[0].end_offset, 5)
