package com.cse3063.rag.answer;

import com.cse3063.rag.orchestrator.PipelineStage;

/**
 * Adapter so answer agents can be used as PipelineStages.
 */
public interface AnswerAgent extends PipelineStage {
	// Inherits Context execute(Context) from PipelineStage
}
