import java.util.Map;

/**
 * [GRASP - Creator]
 * [SOLID - Dependency Inversion Principle]
 * Responsible for instantiating concrete strategies based on configuration.
 */
public class StageFactory {

    private final Map<String, Object> appConfig;

    public StageFactory(Map<String, Object> appConfig) {
        this.appConfig = appConfig;
    }

    public PipelineStage createStage(String stageType) {
        // In a real dynamic system, we would use Class.forName() and reflection here
        // based on the config string.
        // For this strict "No Framework" example, we verify the config and return Stubs
        // if the concrete classes aren't available yet.

        // 1. Look up strategy name from config
        // Map<String, Object> stagesConfig = (Map<String, Object>) appConfig.get("pipeline_stages");
        // Map<String, String> specificConfig = (Map<String, String>) stagesConfig.get(stageType);
        // String strategyClass = specificConfig.get("strategy_class");

        // 2. Simple Switch for Demonstration (Replace with Reflection for full OCP)
        System.out.println("FACTORY: initializing " + stageType);

        return new PipelineStage() {
            @Override
            public RagContext execute(RagContext ctx) {
                // DUMMY IMPLEMENTATION FOR DEMO
                if (stageType.equals("intent_detector")) ctx.setCurrentIntent("StaffLookup");
                if (stageType.equals("query_writer")) {
                    ctx.getQueryTerms().add("murat");
                    ctx.getQueryTerms().add("ganiz");
                }
                if (stageType.equals("answer_agent")) ctx.setFinalAnswer("This is a dummy answer from " + stageType);
                return ctx;
            }
            @Override
            public String getName() { return stageType; }
        };
    }
}