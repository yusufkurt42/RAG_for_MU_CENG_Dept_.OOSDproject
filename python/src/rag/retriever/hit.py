from src.rag.model.chunk import Chunk

class Hit:
    """
    Represents a search hit (match).
    GRASP: Information Expert (Manages its own scoring state).
    """
    def __init__(self, chunk: Chunk, initial_score: float):
        self._chunk = chunk
        self._initial_score = initial_score
        self._rerank_score = initial_score

    @property
    def chunk(self) -> Chunk:
        return self._chunk

    @property
    def initial_score(self) -> float:
        return self._initial_score

    @property
    def rerank_score(self) -> float:
        return self._rerank_score

    @rerank_score.setter
    def rerank_score(self, score: float):
        self._rerank_score = score

    def __repr__(self):
        return (f"Hit(id='{self._chunk.id}', "
                f"init={self._initial_score:.2f}, "
                f"rerank={self._rerank_score:.2f})")