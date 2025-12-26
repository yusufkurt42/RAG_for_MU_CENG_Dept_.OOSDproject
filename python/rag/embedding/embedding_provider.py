from __future__ import annotations

from dataclasses import dataclass
import hashlib
import math
import re
from typing import List, Protocol


class EmbeddingProvider(Protocol):
    def embed_text(self, text: str) -> List[float]:
        ...

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        ...



@dataclass(frozen=True)
class HashEmbeddingConfig:
    dim: int = 64
    normalize: bool = True
    token_pattern: str = r"[A-Za-zÇĞİÖŞÜçğıöşü0-9]+"
    salt: str = "miniRAG-v1"


class DeterministicHashEmbeddingProvider:
    """
    Deterministic stub embedding:
      - tokenize
      - token -> sha256 -> bucket index + sign
      - accumulate -> dense vector
      - optional L2 normalize
    """

    def __init__(self, cfg: HashEmbeddingConfig | None = None):
        self._cfg = cfg or HashEmbeddingConfig()
        self._token_re = re.compile(self._cfg.token_pattern)

    def embed_text(self, text: str) -> List[float]:
        vec = [0.0] * self._cfg.dim
        tokens = self._token_re.findall((text or "").lower())

        if not tokens:
            return vec

        for tok in tokens:
            h = hashlib.sha256((self._cfg.salt + ":" + tok).encode("utf-8")).digest()
            idx = int.from_bytes(h[0:2], "big") % self._cfg.dim
            sign = 1.0 if (h[2] % 2 == 0) else -1.0
            vec[idx] += sign

        if self._cfg.normalize:
            self._l2_normalize_inplace(vec)

        return vec

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

    @staticmethod
    def _l2_normalize_inplace(vec: List[float]) -> None:
        norm2 = sum(x * x for x in vec)
        if norm2 <= 0.0:
            return
        inv = 1.0 / math.sqrt(norm2)
        for i in range(len(vec)):
            vec[i] *= inv
