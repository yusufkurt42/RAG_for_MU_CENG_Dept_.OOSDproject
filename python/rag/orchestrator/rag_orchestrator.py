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
    
    def answer_question(self, question: str) -> str:
        """
        Process a question through the pipeline.
        
        Args:
            question: User's question
            
        Returns:
            Answer text
        """
        print("--- ORCHESTRATOR: Starting Processing ---")
        
        # Create context
        context = Context(original_question=question)
        
        # Execute pipeline
        try:
            context = self.pipeline.execute(context, self.trace_bus)
        except Exception as e:
            print(f"Pipeline execution failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Ensure logs are flushed
            self.trace_bus.close_all()
        
        print("--- ORCHESTRATOR: Finished ---")
        
        # Return result
        if context and context.final_answer:
            return context.final_answer.text or ""
        else:
            return "Cevap üretilemedi."
