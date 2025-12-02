"""Pipeline execution engine."""

from typing import List
import time
from .context import Context
from .pipeline_stage import PipelineStage
from ..tracer.trace_bus import TraceBus
from ..tracer.trace_event import TraceEvent


class Pipeline:
    """
    Pipeline for executing stages sequentially.
    [GRASP - Pure Fabrication]
    """
    
    def __init__(self):
        """Initialize empty pipeline."""
        self.stages: List[PipelineStage] = []
    
    def add_stage(self, stage: PipelineStage) -> None:
        """Add a stage to the pipeline."""
        self.stages.append(stage)
    
    def execute(self, context: Context, trace_bus: TraceBus) -> Context:
        """
        Execute all stages in order.
        
        Args:
            context: The context object to process
            trace_bus: Trace bus for logging events
            
        Returns:
            Updated context after all stages
        """
        for stage in self.stages:
            start_time = time.time()
            stage_name = stage.get_name()
            success = True
            output_summary = "Success"
            
            try:
                # Execute stage logic
                stage.execute(context)
                
            except Exception as e:
                # Handle failures gracefully
                success = False
                output_summary = f"Error: {str(e)}"
                print(f"[CRITICAL] Pipeline stopped at {stage_name}: {str(e)}")
                import traceback
                traceback.print_exc()
                
            finally:
                # Calculate duration
                duration = time.time() - start_time
                
                # Create trace event
                event = TraceEvent(
                    stage_name=stage_name,
                    input_summary=str(context),
                    output_summary=output_summary,
                    duration_ms=int(duration * 1000)
                )
                
                # Publish to trace bus
                if trace_bus:
                    trace_bus.trace(event)
                
                # Stop pipeline if stage failed
                if not success:
                    break
        
        return context
