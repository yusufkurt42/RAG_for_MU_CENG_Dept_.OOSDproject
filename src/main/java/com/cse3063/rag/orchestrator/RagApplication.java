package com.cse3063.rag.orchestrator;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.util.Map;

public class RagApplication {
    public static void main(String[] args) throws Exception {
        // 1. Load configuration from resources/config.json
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> appConfig = mapper.readValue(new File("src/main/resources/config.json"), new TypeReference<Map<String,Object>>(){});

        // 2. Initialize Controller
        RagOrchestrator orchestrator = new RagOrchestrator(appConfig);

        // 3. Run Scenario
        String question = "Ali Haydar Özer'in maili nedir?";
        String answer = orchestrator.answerQuestion(question);

        // 4. Output
        System.out.println("\nFinal Result:\n" + answer);
    }
}