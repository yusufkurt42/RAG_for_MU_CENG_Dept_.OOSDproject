import java.util.ArrayList;
import java.util.List;

/**
 * [GRASP - Pure Fabrication]
 * Responsible for the mechanics of running stages sequentially.
 * It is decoupled from the specific control flow of the Orchestrator.
 */
public class Pipeline {

    // The list of PipelineStage implementations to execute
    private final List<PipelineStage> stages = new ArrayList<>();

    public void addStage(PipelineStage stage) {
        this.stages.add(stage);
    }

    /**
     * Executes all stages added to the pipeline in order.
     * The Observer (TraceBus) logic should be integrated here or in the Orchestrator.
     */
    public RagContext execute(RagContext context) {
        for (PipelineStage stage : stages) {
            long startTime = System.currentTimeMillis();

            try {
                // Execute the stage logic
                context = stage.execute(context);

                // Publish trace event (Simulated logging)
                long duration = System.currentTimeMillis() - startTime;
                context.addMetadata(stage.getName() + "_time", duration);
                System.out.println(String.format("[TRACE] %s completed in %d ms.", stage.getName(), duration));

            } catch (Exception e) {
                // Publish error trace event
                context.addMetadata(stage.getName() + "_error", e.getMessage());
                System.err.println(String.format("[ERROR] Pipeline stopped at %s: %s", stage.getName(), e.getMessage()));
                break; // Stop pipeline execution on failure
            }
        }
        return context;
    }
}