from abc import abstractmethod
from src.rag.orchestrator.pipeline import PipelineStage

class Retriever(PipelineStage):
    """
    Base Retriever Interface.
    Enforces the contract for any retrieval strategy (Keyword, Vector, Hybrid).
    """
    pass