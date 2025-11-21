package com.cse3063.rag.retrieval;

import com.cse3063.rag.model.Chunk;
import java.util.*;

public class SimpleRetriever implements IRetriever {

    private final KeywordIndex index;

    public SimpleRetriever(KeywordIndex index) {
        this.index = index;
    }

    @Override
    public List<Hit> retrieve(String query, int k) {
        String[] queryTerms = query.toLowerCase().split("\\W+");
        Map<Chunk, Double> scores = new HashMap<>();

        for (String term : queryTerms) {
            Map<Chunk, Integer> matches = index.search(term);
            
            for (Map.Entry<Chunk, Integer> entry : matches.entrySet()) {
                Chunk chunk = entry.getKey();
                int tf = entry.getValue();
                
                // Simple Score
                scores.put(chunk, scores.getOrDefault(chunk, 0.0) + tf);
            }
        }

        // 3. convert map to list and sort
        List<Hit> hits = new ArrayList<>();
        for (Map.Entry<Chunk, Double> entry : scores.entrySet()) {
            hits.add(new Hit(entry.getKey(), entry.getValue()));
        }
        Collections.sort(hits);

        // return first K results
        if (hits.size() > k) {
            return hits.subList(0, k);
        }
        return hits;
    }
}