package com.cse3063.rag.orchestrator;

import java.io.IOException;
import java.util.Map;

import com.cse3063.rag.tracer.JsonlTraceSink;
import com.cse3063.rag.tracer.TraceBus;


/**
 * [GRASP - Controller]
 * Coordinates the RAG process. It constructs the pipeline based on config
 * and manages the flow of the user request.
 */
public class RagOrchestrator {
    private final Pipeline pipeline;
    private final TraceBus traceBus;

    /**
     * Backwards-compatible constructor that accepts a simple JSON/config path string.
     * For now we delegate to the factory that can load or interpret the config.
     */
    public RagOrchestrator(String configPath, String chunkPath) {
        // In this codebase the StageFactory has a constructor overload accepting Map,
        // however some examples pass a simple string. We'll create a minimal map here
        // to preserve compatibility.
        this.pipeline = new Pipeline();

        this.traceBus = new TraceBus();
        this.traceBus.register(new JsonlTraceSink());

        buildPipeline(configPath, chunkPath);
    }

    /**
     * [Pattern - Template Method]
     * Defines the fixed skeleton of the RAG workflow.
     * The order is fixed, but the implementation of each step is variable (Strategy).
     */
    private void buildPipeline(String configPath, String chunkPath) {
        // The order is strictly defined here:
        try {
            pipeline.addStage(ComponentFactory.createIntentDetector(configPath));
            pipeline.addStage(ComponentFactory.createQueryWriter(configPath));
            pipeline.addStage(ComponentFactory.createRetriever(configPath, chunkPath));
            pipeline.addStage(ComponentFactory.createReranker(configPath));
            pipeline.addStage(ComponentFactory.createAnswerAgent(configPath, chunkPath));
        } catch (IOException e) {
            System.err.println("CRITICAL: Failed to build pipeline from config.");
            e.printStackTrace();
        }
    }

    public String answerQuestion(String question) {
        System.out.println("--- ORCHESTRATOR: Starting Processing ---");

        // 1. Create Context (State)
        Context context = new Context(question);

        // 2. Delegate execution to Pipeline AND pass the TraceBus
        // Pipeline stages will use traceBus.trace(...) to log inputs/outputs.
        try {
            context = pipeline.execute(context, traceBus);
        } catch (Exception e) {
            System.err.println("Pipeline execution failed: " + e.getMessage());
            e.printStackTrace();
        } finally {
            // 3. Ensure logs are flushed and closed properly after execution
            traceBus.closeAll();
        }

        // 4. Return Result
        System.out.println("--- ORCHESTRATOR: Finished ---");
        
        if (context == null || context.getFinalAnswer() == null) {
            System.out.println("No final answer produced.");
            return "Cevap üretilemedi.";
        }
        
        String text = context.getFinalAnswer().getText();
        return text == null ? "" : text;
    }
}