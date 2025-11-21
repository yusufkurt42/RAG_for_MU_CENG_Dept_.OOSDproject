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
    RagContext execute(RagContext context);

    /**
     * Returns the name of the stage for tracing/logging.
     */
    String getName();
}