package com.cse3063.rag.retrieval;

import com.cse3063.rag.model.Chunk;

public class Hit implements Comparable<Hit> {
    private final Chunk chunk;
    private final double score;

    public Hit(Chunk chunk, double score) {
        this.chunk = chunk;
        this.score = score;
    }

    public Chunk getChunk() { return chunk; }
    public double getScore() { return score; }

    @Override
    public int compareTo(Hit other) {
        return Double.compare(other.score, this.score);
    }
    
    @Override
    public String toString() {
        return String.format("[Score: %.2f] %s...", score, chunk.getText().substring(0, Math.min(50, chunk.getText().length())));
    }
}