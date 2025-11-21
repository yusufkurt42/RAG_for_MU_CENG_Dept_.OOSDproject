package com.cse3063.rag.orchestrator;

/**
 * [SOLID - Interface Segregation Principle]
 * [SOLID - Dependency Inversion Principle]
 * Defines the contract for any processing step in the RAG pipeline.
 * The Pipeline depends on this abstraction, not concrete implementations.
 */
public interface PipelineStage {
    /**
     * Executes a specific logic on the context.
     * @param context The shared state of the current request.
     * @return The modified context.
     */
    void execute(Context context);

    /**
     * Human readable name of the stage used for tracing/logging.
     */
    String getName();
}