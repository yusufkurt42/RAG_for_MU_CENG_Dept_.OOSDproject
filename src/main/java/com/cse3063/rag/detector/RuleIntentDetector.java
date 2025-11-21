package com.cse3063.rag.detector;

import com.cse3063.rag.orchestrator.Context;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class RuleIntentDetector implements IntentDetector {

    private int[] priority;
    // Map of Intent to Keyword List
    private Map<Intent, List<String>> intentRules;

    public RuleIntentDetector(String jsonFilePath) {
        try {
            loadRules(jsonFilePath);
        } catch (IOException e) {
            System.err.println("Hata: rules.json dosyası okunamadı! " + e.getMessage());
            this.intentRules = Map.of(); 
        }
    }

    private void loadRules(String path) throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        
        // Converts JSON file to Map<Intent, List<String>> structure
        // Jackson library automatically attempts to convert String keys to Enum.
        this.intentRules = mapper.readValue( // ObjectMapper -> Converts JSON -> Java object.
            new File(path), 
            new TypeReference<Map<Intent, List<String>>>() {}
        );
    }

    @Override
    public void execute(Context context) { // Each value held in the priority array represents an intent enum value. The enum value at the
        String question=context.getOriginalQuestion();

        if (question == null || question.trim().isEmpty()) { // first index indicates the highest priority intent.
            context.setCurrentIntent(Intent.UNKNOWN);
        }

        // Case-insensitivity
        String normalizedQuestion = question.toLowerCase();

        List<Intent> candidates = new ArrayList<>();

        // Iterate through every Intent and Keyword list in the Map
        for (Map.Entry<Intent, List<String>> entry : intentRules.entrySet()) {
            Intent intent = entry.getKey(); // Intent = Key, Keywords = Value
            List<String> keywords = entry.getValue();

            // Check every keyword belonging to that Intent
            for (String keyword : keywords) {
                if (normalizedQuestion.contains(keyword.toLowerCase())) {
                    candidates.add(intent);
                    break;
                }
            }
        }

        // If there are no candidates
        if (candidates.isEmpty()) {
            context.setCurrentIntent(Intent.UNKNOWN);
        }

        // If there is only 1 candidate, return it directly
        if (candidates.size() == 1) {
            context.setCurrentIntent(candidates.get(0));
        }
        
        
        
        if (priority != null) {
            // Check candidates according to the order in the priority list
            for (int intentOrdinal : priority) { // The position in the array determines the priority, not the values held.
                // Converting int value to Enum
                // (Note: Must ensure numbers in the array are valid Enum IDs)
                if (intentOrdinal >= 0 && intentOrdinal < Intent.values().length) {
                    Intent priorityIntent = Intent.values()[intentOrdinal];
                    
                    // If this priority Intent exists in our candidate list, it is the winner.
                    if (candidates.contains(priorityIntent)) {
                        context.setCurrentIntent(priorityIntent);
                    }
                }
            }
        }

        // If priority list is not provided or those in the list are not among the candidates
        // Return the first one found by default.
        context.setCurrentIntent(candidates.get(0));
    }

    @Override
    public String getName() { return "intent_detector"; }
}