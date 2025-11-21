package com.cse3063.rag.orchestrator;

import com.cse3063.rag.tracer.TraceBus;
import com.cse3063.rag.tracer.TraceEvent;

import java.util.ArrayList;
import java.util.List;

/**
 * [GRASP - Pure Fabrication]
 * Responsible for the mechanics of running stages sequentially.
 * It is decoupled from the specific control flow of the Orchestrator.
 */
public class Pipeline {

    // The list of PipelineStage implementations to execute (Strategy Pattern)
    private final List<PipelineStage> stages = new ArrayList<>();

    public void addStage(PipelineStage stage) {
        this.stages.add(stage);
    }

    /**
     * Executes all stages added to the pipeline in order.
     * FIX: Updated to accept TraceBus for proper Observer pattern integration.
     */
    public Context execute(Context context, TraceBus traceBus) {
        
        for (PipelineStage stage : stages) {
            long startTime = System.currentTimeMillis();
            String stageName = stage.getName(); // e.g., "IntentDetector"
            boolean success = true;
            String outputSummary = "Success";

            try {
                // 1. Execute the stage logic
                stage.execute(context);

            } catch (Exception e) {
                // Handle failures gracefully in the trace
                success = false;
                outputSummary = "Error: " + e.getMessage();
                
                // Print critical error to stderr for immediate visibility
                System.err.println(String.format("[CRITICAL] Pipeline stopped at %s: %s", stageName, e.getMessage()));
                e.printStackTrace();
            } finally {
                // 2. Calculate Duration
                long duration = System.currentTimeMillis() - startTime;

                // 3. Create Trace Event (Inputs/Outputs can be refined based on Context state)
                // For Iteration 1, we log the stage name and success status.
                TraceEvent event = new TraceEvent(
                    stageName,
                    "Context(Input)",   // Girdi özeti
                    outputSummary,      // Çıktı özeti veya Hata mesajı
                    duration
                );

                // 4. Publish to Bus (Observer Pattern)
                if (traceBus != null) {
                    traceBus.trace(event);
                }

                // If the stage failed, stop the pipeline to prevent cascading errors.
                if (!success) {
                    break; 
                }
            }
        }
        return context;
    }
}