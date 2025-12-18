from __future__ import annotations

from dataclasses import dataclass
import math
from typing import List, Sequence, Tuple


@dataclass(frozen=True)
class VectorIndexConfig:
    top_k_default: int = 10


@dataclass(frozen=True)
class VectorEntry:
    chunk_id: str
    vector: List[float]


class VectorIndex:
    """In-memory vector index stub (cosine similarity)."""

    def __init__(self, cfg: VectorIndexConfig | None = None):
        self._cfg = cfg or VectorIndexConfig()
        self._entries: List[VectorEntry] = []

    def add(self, chunk_id: str, vector: List[float]) -> None:
        self._entries.append(VectorEntry(chunk_id=chunk_id, vector=vector))

    def add_many(self, items: Sequence[Tuple[str, List[float]]]) -> None:
        for cid, vec in items:
            self.add(cid, vec)

    def search(self, query_vec: List[float], top_k: int | None = None) -> List[Tuple[str, float]]:
        k = top_k or self._cfg.top_k_default
        scored: List[Tuple[str, float]] = []

        for e in self._entries:
            score = self._cosine(query_vec, e.vector)
            scored.append((e.chunk_id, score))

        # deterministic tie-break: score desc, chunk_id asc
        scored.sort(key=lambda x: (-x[1], x[0]))
        return scored[:k]

    @staticmethod
    def _cosine(a: List[float], b: List[float]) -> float:
        dot = 0.0
        na = 0.0
        nb = 0.0
        m = min(len(a), len(b))
        for i in range(m):
            dot += a[i] * b[i]
            na += a[i] * a[i]
            nb += b[i] * b[i]
        if na <= 0.0 or nb <= 0.0:
            return 0.0
        return dot / math.sqrt(na * nb)
