"""Tests for chunker."""

import pytest
from rag.chunker import SlidingWindowChunker


class TestSlidingWindowChunker:
    """Test cases for SlidingWindowChunker."""
    
    def test_basic_chunking(self):
        """Test basic chunking functionality."""
        chunker = SlidingWindowChunker(window_size=10, overlap=2)
        text = "This is a test text for chunking"
        
        chunks = chunker.chunk("doc1", text)
        
        assert len(chunks) > 0
        assert all(chunk.doc_id == "doc1" for chunk in chunks)
    
    def test_overlap(self):
        """Test overlap between chunks."""
        chunker = SlidingWindowChunker(window_size=10, overlap=5)
        text = "0123456789ABCDEFGHIJ"
        
        chunks = chunker.chunk("doc1", text)
        
        # Should have overlap
        assert len(chunks) >= 2
    
    def test_empty_text(self):
        """Test empty text."""
        chunker = SlidingWindowChunker(window_size=10, overlap=2)
        
        chunks = chunker.chunk("doc1", "")
        
        assert chunks == []
    
    def test_invalid_overlap(self):
        """Test invalid overlap configuration."""
        with pytest.raises(ValueError):
            SlidingWindowChunker(window_size=10, overlap=10)
    
    def test_chunk_ids(self):
        """Test chunk ID generation."""
        chunker = SlidingWindowChunker(window_size=10, overlap=2)
        text = "This is a test text for chunking"
        
        chunks = chunker.chunk("doc1", text)
        
        # Check IDs are unique and sequential
        ids = [chunk.id for chunk in chunks]
        assert len(ids) == len(set(ids))  # All unique
        assert all("doc1" in chunk_id for chunk_id in ids)
