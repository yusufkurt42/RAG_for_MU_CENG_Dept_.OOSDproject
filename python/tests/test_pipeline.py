
import unittest
from rag.orchestrator.pipeline import Pipeline
from rag.orchestrator.context import Context
from rag.orchestrator.pipeline_stage import PipelineStage
from unittest.mock import MagicMock

class MockStage(PipelineStage):
    def __init__(self, name, should_fail=False):
        self.name = name
        self.should_fail = should_fail
        self.executed = False
        
    def execute(self, context: Context) -> None:
        self.executed = True
        if self.should_fail:
            raise Exception("Stage failed")
            
    def get_name(self) -> str:
        return self.name

class TestPipeline(unittest.TestCase):
    def test_pipeline_execution(self):
        pipeline = Pipeline()
        stage1 = MockStage("stage1")
        stage2 = MockStage("stage2")
        
        pipeline.add_stage(stage1)
        pipeline.add_stage(stage2)
        
        context = Context(original_question="test")
        pipeline.execute(context, trace_bus=None)
        
        self.assertTrue(stage1.executed)
        self.assertTrue(stage2.executed)
        
    def test_pipeline_failure(self):
        pipeline = Pipeline()
        stage1 = MockStage("stage1", should_fail=True)
        stage2 = MockStage("stage2")
        
        pipeline.add_stage(stage1)
        pipeline.add_stage(stage2)
        
        context = Context(original_question="test")
        pipeline.execute(context, trace_bus=None)
        
        self.assertTrue(stage1.executed)
        self.assertFalse(stage2.executed) # Should stop after failure
