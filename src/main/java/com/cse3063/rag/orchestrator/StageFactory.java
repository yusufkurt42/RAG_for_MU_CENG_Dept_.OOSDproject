package com.cse3063.rag.orchestrator;

import java.util.Map;
import java.util.Collections;

/**
 * [GRASP - Creator]
 * [SOLID - Dependency Inversion Principle]
 * Responsible for instantiating concrete strategies based on configuration.
 */
public class StageFactory {

    @SuppressWarnings("unused")
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

        try {
            switch (stageType) {
                case "intent_detector":
                    // Provide a simple path or use defaults; the RuleIntentDetector will fallback if file missing
                    return new com.cse3063.rag.detector.RuleIntentDetector("src/main/resources/rules.json");
                case "query_writer":
                    // Build a simple HeuristicQueryWriter with empty stopwords/boosters
                    return new com.cse3063.rag.writer.HeuristicQueryWriter(Collections.emptyList(), Collections.emptyMap(), Collections.emptyList());
                case "answer_agent":
                    return new com.cse3063.rag.answer.TemplateAnswerAgent();
                default:
                    // fallback anonymous stage
                    return new PipelineStage() {
                        @Override
                        public void execute(Context ctx){return;}

                        @Override
                        public String getName() { return stageType; }
                    };
            }
        } catch (Exception e) {
            System.err.println("FACTORY: error creating stage " + stageType + ": " + e.getMessage());
            return new PipelineStage() {
                @Override
                public void execute(Context ctx){return;}
                @Override
                public String getName() { return stageType; }
            };
        }
    }
}