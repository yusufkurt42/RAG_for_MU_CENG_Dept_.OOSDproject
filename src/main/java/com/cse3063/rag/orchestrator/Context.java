package com.cse3063.rag.orchestrator;

import com.cse3063.rag.answer.Answer;
import com.cse3063.rag.retriever.Hit;
import com.cse3063.rag.detector.Intent;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * [GRASP - Information Expert]
 * Holds the state of the request as it flows through the pipeline.
 * It is the "Expert" on the current execution data.
 */
public class Context {
    private final String originalQuestion;

    // Pipeline State
    private Intent currentIntent = Intent.UNKNOWN;
    private List<String> queryTerms = new ArrayList<>();

    // We use Maps to represent Hits to avoid creating a 'Hit' class dependency for now,
    // but in a real scenario, List<Hit> is preferred.
    private List<Hit> retrievalHits = new ArrayList<>();

    private Answer finalAnswer=null;
    private Map<String, Object> metadata = new HashMap<>();

    public Context(String originalQuestion) {
        this.originalQuestion = originalQuestion;
    }

    // --- Getters and Setters ---

    public String getOriginalQuestion() { return originalQuestion; }

    public Intent getCurrentIntent() { return currentIntent; }
    public void setCurrentIntent(Intent currentIntent) { this.currentIntent = currentIntent; }

    public List<String> getQueryTerms() { return queryTerms; }
    public void setQueryTerms(List<String> queryTerms) { this.queryTerms = queryTerms; }

    public List<Hit> getRetrievalHits() { return retrievalHits; }
    public void setRetrievalHits(List<Hit> retrievalHits) { this.retrievalHits = retrievalHits; }

    public Answer getFinalAnswer() { return finalAnswer; }
    public void setFinalAnswer(Answer finalAnswer) { this.finalAnswer = finalAnswer; }

    public void addMetadata(String key, Object value) { this.metadata.put(key, value); }
    public Object getMetadata(String key) { return this.metadata.get(key); }

    @Override
    public String toString() {
        return String.format("Context{Intent='%s', Terms=%s, Hits=%d, Answer='%s'}",
                currentIntent, queryTerms, retrievalHits.size(), finalAnswer);
    }

    public void setTermsList(List<String> terms) {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'setTermsList'");
    }
}