package com.cse3063.rag.retriever;

import com.cse3063.rag.model.Chunk;

/**
 * Hit: Represents a single matched content chunk, holding a direct reference 
 * to the Chunk and associated scoring metadata.
 * * This object is created by the Retriever and modified by the Reranker.
 */
public class Hit {

    // --- Core Data Reference ---
    // Holding the Chunk reference allows the Reranker and AnswerAgent 
    // immediate access to content and metadata without querying the ChunkStore repeatedly.
    private final Chunk chunk; 
    
    // --- Scoring & Ranking Metadata ---
    
    // The initial score calculated by the Retriever (e.g., TF sum).
    private final double initialScore;
    
    // The final score assigned by the Reranker after applying bonuses (e.g., proximity/title boost).
    private double rerankScore;

    /**
     * Constructor used typically by the Retriever when the Hit is first generated.
     */
    public Hit(Chunk chunk, double initialScore) {
        this.chunk = chunk;
        this.initialScore = initialScore;
        // Initially, the rerank score is set to the initial score.
        this.rerankScore = initialScore; 
    }

    // --- Getters ---

    public Chunk getChunk() {
        return chunk;
    }

    public double getInitialScore() {
        return initialScore;
    }

    public double getRerankScore() {
        return rerankScore;
    }

    // --- Setter (Necessary for the Reranker component) ---
    
    /**
     * Allows the Reranker component to update the final ranking score.
     */
    public void setRerankScore(double rerankScore) {
        this.rerankScore = rerankScore;
    }

    @Override
    public String toString() {
        return "Hit{" +
                "chunkId='" + chunk.getId() + '\'' + // Assuming Chunk has a getId() method
                ", initialScore=" + initialScore +
                ", rerankScore=" + rerankScore +
                '}';
    }
}