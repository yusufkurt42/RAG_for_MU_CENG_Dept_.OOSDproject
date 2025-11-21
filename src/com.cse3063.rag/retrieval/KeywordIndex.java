package com.cse3063.rag.retrieval;

import com.cse3063.rag.model.Chunk;
import java.util.*;

public class KeywordIndex {
    private final Map<String, Map<Chunk, Integer>> invertedIndex = new HashMap<>();
    private final List<Chunk> allChunks;

    public KeywordIndex(List<Chunk> chunks) {
        this.allChunks = chunks;
        buildIndex();
    }

    private void buildIndex() {
        for (Chunk chunk : allChunks) {
            String[] terms = chunk.getText().toLowerCase().split("\\W+");
            for (String term : terms) {
                if (term.length() < 3) continue;	//short terms not important

                invertedIndex.putIfAbsent(term, new HashMap<>());
                Map<Chunk, Integer> postings = invertedIndex.get(term);
                
                postings.put(chunk, postings.getOrDefault(chunk, 0) + 1);
            }
        }
        System.out.println("Index oluşturuldu. Toplam kelime sayısı: " + invertedIndex.size());
    }

    public Map<Chunk, Integer> search(String term) {
        return invertedIndex.getOrDefault(term.toLowerCase(), Collections.emptyMap());
    }
}