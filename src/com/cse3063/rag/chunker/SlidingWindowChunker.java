package com.cse3063.rag.chunker;

import com.cse3063.rag.chunker.IChunker;
import com.cse3063.rag.model.Chunk;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class SlidingWindowChunker implements IChunker {
    
    private final int windowSize;
    private final int overlap;

    public SlidingWindowChunker(int windowSize, int overlap) {
        if (overlap >= windowSize) {
            throw new IllegalArgumentException("Overlap cannot be greater than or equal to windowSize.");
        }
        this.windowSize = windowSize;
        this.overlap = overlap;
    }

    @Override
    public List<Chunk> chunk(String docId, String fullText) {
        List<Chunk> chunks = new ArrayList<>();
        
        if (fullText == null || fullText.isEmpty()) {
            return chunks;
        }

        int textLength = fullText.length();
        int start = 0;

        while (start < textLength) {
            int end = Math.min(start + windowSize, textLength);
            
            String chunkText = fullText.substring(start, end);

            String normalizedText = chunkText.toLowerCase().trim();

            String chunkId = docId + "_" + (chunks.size() + 1); 
            
            chunks.add(new Chunk(
                chunkId,
                docId,
                normalizedText,
                start,
                end
            ));

            if (end == textLength) {
                break;
            }
            
            start += (windowSize - overlap);
        }

        return chunks;
    }
}