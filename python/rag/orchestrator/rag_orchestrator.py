"""RAG orchestrator - main controller."""

from .pipeline import Pipeline
from .context import Context
from .component_factory import ComponentFactory
from ..tracer import TraceBus, JsonlTraceSink


class RagOrchestrator:
    """
    RAG Orchestrator coordinates the entire RAG workflow.
    [GRASP - Controller]
    """
    
    def __init__(self, config_path: str, chunk_path: str = ""):
        """
        Initialize orchestrator.
        
        Args:
            config_path: Path to configuration file
            chunk_path: Optional path to chunk file
        """
        self.pipeline = Pipeline()
        self.trace_bus = TraceBus()
        self.trace_bus.register(JsonlTraceSink())
        
        self._build_pipeline(config_path, chunk_path)
    
    def _build_pipeline(self, config_path: str, chunk_path: str = "") -> None:
        """
        Build the pipeline with components.
        [Pattern - Template Method]
        """
        try:
            # Add stages in fixed order
            self.pipeline.add_stage(ComponentFactory.create_intent_detector(config_path))
            self.pipeline.add_stage(ComponentFactory.create_query_writer(config_path))
            self.pipeline.add_stage(ComponentFactory.create_retriever(config_path, chunk_path))
            self.pipeline.add_stage(ComponentFactory.create_reranker(config_path))
            self.pipeline.add_stage(ComponentFactory.create_answer_agent(config_path, chunk_path))
        except Exception as e:
            print(f"CRITICAL: Failed to build pipeline from config: {e}")
            raise
    
    def answer_question(self, question: str): # Returns Answer object, not just string
        """
        Process a question through the pipeline.
        """
        print(f"--- ORCHESTRATOR: Processing '{question[:30]}...' ---")
        
        context = Context(original_question=question)
        
        try:
            # Execute pipeline without closing the bus immediately
            context = self.pipeline.execute(context, self.trace_bus)
        except Exception as e:
            print(f"Pipeline execution failed: {e}")
            import traceback
            traceback.print_exc()
        
        # REMOVED: self.trace_bus.close_all() from here.
        # It must be closed explicitly by the caller (main.py) after batch finishes.
        
        print("--- ORCHESTRATOR: Finished ---")
        
        # Return the full Answer object to access citations in main.py
        if context and context.final_answer:
            return context.final_answer
        else:
            from ..answer.answer import Answer
            return Answer(text="No answer generated.", citations=[])

    def close(self):
        """Explicitly close resources (logs)."""
        if self.trace_bus:
            self.trace_bus.close_all()
