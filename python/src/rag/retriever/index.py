import re
from typing import List, Dict
from src.rag.model.chunk import Chunk

class KeywordIndex:
    """
    Inverted Index implementation for keyword search.
    SRP: Handles indexing and basic lookups only.
    """
    def __init__(self, chunks: List[Chunk]):
        self._inverted_index: Dict[str, Dict[Chunk, int]] = {}
        self._all_chunks = chunks
        self._build_index()

    def _build_index(self):
        print("Building index...")
        for chunk in self._all_chunks:
            terms = re.split(r'\W+', chunk.text.lower())
            for term in terms:
                if len(term) < 3: continue
                
                if term not in self._inverted_index:
                    self._inverted_index[term] = {}
                
                postings = self._inverted_index[term]
                postings[chunk] = postings.get(chunk, 0) + 1
        print(f"Index built. Unique terms: {len(self._inverted_index)}")

    def search(self, term: str) -> Dict[Chunk, int]:
        return self._inverted_index.get(term.lower(), {})