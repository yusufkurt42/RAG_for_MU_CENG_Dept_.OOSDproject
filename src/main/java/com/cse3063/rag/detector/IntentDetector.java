package com.cse3063.rag.detector;
import com.cse3063.rag.orchestrator.Context;
import com.cse3063.rag.orchestrator.PipelineStage;

/**
 * Adapter interface so intent detectors are also PipelineStages.
 */
public interface IntentDetector extends PipelineStage {
    void execute(Context context);
}