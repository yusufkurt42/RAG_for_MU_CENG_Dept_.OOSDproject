"""RAG orchestrator - main controller."""

from .pipeline import Pipeline
from .context import Context
from .component_factory import ComponentFactory
from ..tracer import TraceBus, JsonlTraceSink
from ..tracer.trace_event import TraceEvent
import time
import concurrent.futures


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
        #print("--- ORCHESTRATOR: Starting Processing ---")
        
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
        
        #print("--- ORCHESTRATOR: Finished ---")
        
        # Return result
        if context and context.final_answer:
            return context.final_answer.text or ""
        else:
            return "Cevap üretilemedi."

    def answer_questions(self, questions: list) -> list:
        """
        Process a list of questions through the pipeline and return list of answers.

        This method will execute the pipeline separately for each question and
        return their answers in the same order. Reuses the constructed pipeline
        and trace bus for efficiency.
        """
        results = []

        # If there are no stages, nothing to do
        if not self.pipeline.stages:
            return ["Cevap üretilemedi." for _ in questions]

        # Split pipeline into pre-answer stages and the final answer stage
        if len(self.pipeline.stages) == 1:
            pre_stages = []
            answer_stage = self.pipeline.stages[0]
        else:
            pre_stages = self.pipeline.stages[:-1]
            answer_stage = self.pipeline.stages[-1]

        # Pre-process each question sequentially through all stages except the answer stage
        contexts = []
        for q in questions:
            ctx = Context(original_question=q)
            failed = False
            for stage in pre_stages:
                start_time = time.time()
                stage_name = stage.get_name()
                success = True
                output_summary = "Success"
                try:
                    stage.execute(ctx)
                except Exception as e:
                    success = False
                    output_summary = f"Error: {str(e)}"
                    print(f"[CRITICAL] Pipeline stopped at {stage_name} for question '{q}': {str(e)}")
                    import traceback
                    traceback.print_exc()
                finally:
                    duration = time.time() - start_time
                    event = TraceEvent(
                        stage_name=stage_name,
                        input_summary=str(ctx),
                        output_summary=output_summary,
                        duration_ms=int(duration * 1000)
                    )
                    if self.trace_bus:
                        self.trace_bus.trace(event)
                    if not success:
                        failed = True
                        break
            contexts.append(ctx)

        # Run the final answer stage in parallel across contexts
        def run_answer(ctx):
            start_time = time.time()
            stage_name = answer_stage.get_name()
            success = True
            output_summary = "Success"
            try:
                answer_stage.execute(ctx)
            except Exception as e:
                success = False
                output_summary = f"Error: {str(e)}"
                print(f"[ERROR] Answer stage failed for question '{ctx.original_question}': {e}")
                import traceback
                traceback.print_exc()
            finally:
                duration = time.time() - start_time
                event = TraceEvent(
                    stage_name=stage_name,
                    input_summary=str(ctx),
                    output_summary=output_summary,
                    duration_ms=int(duration * 1000)
                )
                if self.trace_bus:
                    self.trace_bus.trace(event)
            return ctx

        # Limit workers to a sensible number to avoid overwhelming local LLM endpoints
        max_workers = min(8, max(1, len(contexts)))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(run_answer, c) for c in contexts]
            # Collect completed contexts in original order
            completed = [f.result() for f in futures]

        for ctx in completed:
            if ctx and ctx.final_answer:
                results.append(ctx.final_answer.text or "")
            else:
                results.append("Cevap üretilemedi.")

        # Ensure logs are flushed after batch
        try:
            self.trace_bus.close_all()
        except Exception:
            pass

        return results
