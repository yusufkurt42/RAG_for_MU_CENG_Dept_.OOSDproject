package com.cse3063.rag.orchestrator;

import java.util.Map;

/**
 * [GRASP - Controller]
 * Coordinates the RAG process. It constructs the pipeline based on config
 * and manages the flow of the user request.
 */
public class RagOrchestrator {
    private final StageFactory factory;
    private final Pipeline pipeline;

    /**
     * Backwards-compatible constructor that accepts a simple JSON/config path string.
     * For now we delegate to the factory that can load or interpret the config.
     */
    public RagOrchestrator(String configPath) {
        // In this codebase the StageFactory has a constructor overload accepting Map,
        // however some examples pass a simple string. We'll create a minimal map here
        // to preserve compatibility.
        this.pipeline = new Pipeline();

        buildPipeline(configPath);
    }

    /**
     * Preferred constructor that accepts an already-parsed application configuration.
     */
    public RagOrchestrator(Map<String, Object> appConfig) {
        this.pipeline = new Pipeline();

        buildPipeline();
    }

    /**
     * [Pattern - Template Method]
     * Defines the fixed skeleton of the RAG workflow.
     * The order is fixed, but the implementation of each step is variable (Strategy).
     */
    private void buildPipeline(String configPath) {
        // The order is strictly defined here:
        pipeline.addStage(ComponentFactory.createIntentDetector(configPath));
        pipeline.addStage(ComponentFactory.createQueryWriter(configPath));
        pipeline.addStage(ComponentFactory.createRetriever(configPath));
        pipeline.addStage(ComponentFactory.createReranker(configPath));
        pipeline.addStage(ComponentFactory.createAnswerAgent(configPath));
    }

    public String answerQuestion(String question) {
        System.out.println("--- ORCHESTRATOR: Starting Processing ---");

        // 1. Create Context (State)
        Context context = new Context(question);

        // 2. Delegate execution to Pipeline
        context = pipeline.execute(context);

        // 3. Return Result (handle nulls safely)
        System.out.println("--- ORCHESTRATOR: Finished ---");
        if (context == null) return "";
        if (context.getFinalAnswer() == null) {
            System.out.println("No final answer produced. Context dump: " + context);
            return "";
        }
        String text = context.getFinalAnswer().getText();
        return text == null ? "" : text;
    }
}