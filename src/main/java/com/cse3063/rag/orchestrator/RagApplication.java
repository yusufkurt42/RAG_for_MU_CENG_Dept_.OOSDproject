package com.cse3063.rag.orchestrator;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.util.Map;

public class RagApplication {
    public static void main(String[] args) throws Exception {
        // 1. Get config and chunks paths
        String chunkPath = "src/main/resources/chunks.json";
        String configPath = "src/main/resources/config.json";

        // 2. Initialize Controller
        RagOrchestrator orchestrator = new RagOrchestrator(configPath, chunkPath);

        // 3. Run Scenario
        String question = "Ali Haydar Özer'in maili nedir?";
        String answer = orchestrator.answerQuestion(question);

        // 4. Output
        System.out.println("\nFinal Result:\n" + answer);
    }
}