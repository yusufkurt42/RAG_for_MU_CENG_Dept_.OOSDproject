from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, TYPE_CHECKING

from ..model import Chunk, ChunkStore
from .hit import Hit
from .vector_index import VectorIndex
from ..embedding import EmbeddingProvider

if TYPE_CHECKING:
    from ..orchestrator.context import Context


@dataclass(frozen=True)
class VectorRetrieverConfig:
    k: int = 10


class VectorRetriever:
    """Vector-based retriever using a VectorIndex + EmbeddingProvider."""

    def __init__(self, chunk_store: ChunkStore, index: VectorIndex, embedder: EmbeddingProvider, cfg: VectorRetrieverConfig | None = None):
        self.chunk_store = chunk_store
        self.index = index
        self.embedder = embedder
        self.cfg = cfg or VectorRetrieverConfig()

        # chunk_id -> Chunk map for fast hit materialization
        self._chunk_by_id: Dict[str, Chunk] = {c.id: c for c in self.chunk_store.get_all_chunks()}

    def execute(self, context: Context) -> None:
        query_terms = context.query_terms
        if not query_terms:
            context.retrieval_hits = []
            return

        query_text = " ".join([t for t in query_terms if t])
        qv = self.embedder.embed_text(query_text)

        results = self.index.search(qv, top_k=self.cfg.k)

        hits: List[Hit] = []
        for chunk_id, score in results:
            chunk = self._chunk_by_id.get(chunk_id)
            if chunk is None:
                continue
            hits.append(Hit(chunk=chunk, initial_score=score))

        context.retrieval_hits = hits
        print(f"   -> Retriever found {len(hits)} results")

    def get_name(self) -> str:
        return "VectorRetriever"
