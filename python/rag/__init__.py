"""RAG package initialization."""

__version__ = "1.0.0"

from .model import Chunk, ChunkStore
from .config import RagConfiguration, JsonConfigLoader
from .detector import Intent, IntentDetector, RuleIntentDetector
from .chunker import IChunker, SlidingWindowChunker
from .writer import QueryWriter, HeuristicQueryWriter
from .retriever import Hit, KeywordIndex, Retriever, SimpleRetriever
from .reranker import Reranker, PhraseAwareReranker
from .answer import Answer, AnswerAgent, TemplateAnswerAgent
from .orchestrator import RagOrchestrator, Context, Pipeline
from .tracer import TraceBus, TraceEvent, TraceSink, JsonlTraceSink
from .store import JsonChunkStore
from .utility import ChunkStoreLoader, JsonConfigLoader

__all__ = [
    # Model
    'Chunk',
    'ChunkStore',
    # Config
    'RagConfiguration',
    'JsonConfigLoader',
    # Detector
    'Intent',
    'IntentDetector',
    'RuleIntentDetector',
    # Chunker
    'IChunker',
    'SlidingWindowChunker',
    # Writer
    'QueryWriter',
    'HeuristicQueryWriter',
    # Retriever
    'Hit',
    'KeywordIndex',
    'Retriever',
    'SimpleRetriever',
    # Reranker
    'Reranker',
    'PhraseAwareReranker',
    # Answer
    'Answer',
    'AnswerAgent',
    'TemplateAnswerAgent',
    # Orchestrator
    'RagOrchestrator',
    'Context',
    'Pipeline',
    # Tracer
    'TraceBus',
    'TraceEvent',
    'TraceSink',
    'JsonlTraceSink',
    # Store
    'JsonChunkStore',
    # Utility
    'ChunkStoreLoader',
]
