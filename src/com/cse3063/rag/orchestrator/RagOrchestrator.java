
import java.util.Map;

/**
 * [GRASP - Controller]
 * Coordinates the RAG process. It constructs the pipeline based on config
 * and manages the flow of the user request.
 */
public class RagOrchestrator {
    private final StageFactory factory;
    private final Pipeline pipeline;

    public RagOrchestrator(Map<String, Object> config) {
        this.factory = new StageFactory(config);
        this.pipeline = new Pipeline();

        buildPipeline();
    }

    /**
     * [Pattern - Template Method]
     * Defines the fixed skeleton of the RAG workflow.
     * The order is fixed, but the implementation of each step is variable (Strategy).
     */
    private void buildPipeline() {
        // The order is strictly defined here:
        pipeline.addStage(factory.createStage("intent_detector"));
        pipeline.addStage(factory.createStage("query_writer"));
        pipeline.addStage(factory.createStage("retriever"));
        pipeline.addStage(factory.createStage("reranker"));
        pipeline.addStage(factory.createStage("answer_agent"));
    }

    public String answerQuestion(String question) {
        System.out.println("--- ORCHESTRATOR: Starting Processing ---");

        // 1. Create Context (State)
        RagContext context = new RagContext(question);

        // 2. Delegate execution to Pipeline
        context = pipeline.execute(context);

        // 3. Return Result
        System.out.println("--- ORCHESTRATOR: Finished ---");
        return context.getFinalAnswer();
    }
}