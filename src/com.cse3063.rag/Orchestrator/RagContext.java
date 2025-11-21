import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * [GRASP - Information Expert]
 * Holds the state of the request as it flows through the pipeline.
 * It is the "Expert" on the current execution data.
 */
public class RagContext {
    private final String originalQuestion;

    // Pipeline State
    private String currentIntent = "Unknown";
    private List<String> queryTerms = new ArrayList<>();

    // We use Maps to represent Hits to avoid creating a 'Hit' class dependency for now,
    // but in a real scenario, List<Hit> is preferred.
    private List<Map<String, String>> retrievalHits = new ArrayList<>();

    private String finalAnswer = "";
    private Map<String, Object> metadata = new HashMap<>();

    public RagContext(String originalQuestion) {
        this.originalQuestion = originalQuestion;
    }

    // --- Getters and Setters ---

    public String getOriginalQuestion() { return originalQuestion; }

    public String getCurrentIntent() { return currentIntent; }
    public void setCurrentIntent(String currentIntent) { this.currentIntent = currentIntent; }

    public List<String> getQueryTerms() { return queryTerms; }
    public void setQueryTerms(List<String> queryTerms) { this.queryTerms = queryTerms; }

    public List<Map<String, String>> getRetrievalHits() { return retrievalHits; }
    public void setRetrievalHits(List<Map<String, String>> retrievalHits) { this.retrievalHits = retrievalHits; }

    public String getFinalAnswer() { return finalAnswer; }
    public void setFinalAnswer(String finalAnswer) { this.finalAnswer = finalAnswer; }

    public void addMetadata(String key, Object value) { this.metadata.put(key, value); }
    public Object getMetadata(String key) { return this.metadata.get(key); }

    @Override
    public String toString() {
        return String.format("Context{Intent='%s', Terms=%s, Hits=%d, Answer='%s'}",
                currentIntent, queryTerms, retrievalHits.size(), finalAnswer);
    }
}