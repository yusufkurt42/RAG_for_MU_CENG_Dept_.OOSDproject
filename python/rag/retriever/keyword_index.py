"""Keyword index for retrieval."""

from __future__ import annotations
from typing import Dict, List, Any
from collections import defaultdict
from ..model import Chunk


class KeywordIndex:
    """Inverted index for keyword-based retrieval (serializable)."""

    def __init__(self):
        # term -> {chunk_id -> tf}
        self.index: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        # chunk_id -> Chunk (for returning Chunk objects to retriever)
        self._chunk_by_id: Dict[str, Chunk] = {}

    def attach_chunks(self, chunks: List[Chunk]) -> None:
        """Attach chunk objects so search() can return Chunk keys."""
        self._chunk_by_id = {c.id: c for c in chunks}

    def add_chunk(self, chunk: Chunk) -> None:
        """Add a chunk to the index."""
        if not chunk.text:
            return

        self._chunk_by_id[chunk.id] = chunk

        # Tokenize (same simple tokenization as before)
        terms = chunk.text.lower().split()
        for term in terms:
            if term:
                self.index[term][chunk.id] += 1

    def search(self, term: str) -> Dict[Chunk, int]:
        """
        Search for chunks containing the term.
        Returns Dict[Chunk, tf] to stay compatible with SimpleRetriever.
        """
        postings = self.index.get(term.lower(), {})
        out: Dict[Chunk, int] = {}
        for cid, tf in postings.items():
            ch = self._chunk_by_id.get(cid)
            if ch is not None:
                out[ch] = tf
        return out

    def build_from_chunks(self, chunks: List[Chunk]) -> None:
        """Build index from a list of chunks."""
        # clear
        self.index = defaultdict(lambda: defaultdict(int))
        self.attach_chunks(chunks)

        for chunk in chunks:
            self.add_chunk(chunk)

    @classmethod
    def load_from_dict(cls, data: Dict[str, Any]) -> "KeywordIndex":
        """
        Load index from dict.
        Supports the on-disk format:
          term -> list[{docId, chunkId, tf}]
        """
        idx = cls()

        for term, entries in (data or {}).items():
            # entries: list of {"docId":..., "chunkId":..., "tf":...}
            if not isinstance(entries, list):
                continue
            term_l = term.lower()
            for e in entries:
                if not isinstance(e, dict):
                    continue
                cid = e.get("chunkId")
                tf = e.get("tf", 0)
                if cid and isinstance(tf, int) and tf > 0:
                    idx.index[term_l][cid] += tf

        # NOTE: chunks are not embedded here; caller must call attach_chunks(chunks)
        return idx
