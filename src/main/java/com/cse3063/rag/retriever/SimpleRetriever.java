package com.cse3063.rag.retriever;

import com.cse3063.rag.orchestrator.PipelineStage;
import com.cse3063.rag.orchestrator.Context;
import com.cse3063.rag.model.Chunk;
import java.util.*;

public class SimpleRetriever implements Retriever {

    private final KeywordIndex index;
    private final int k; // How many results we want

    public SimpleRetriever(KeywordIndex index, int k) {
        this.index = index;
        this.k = k;
    }

    @Override
    public void execute(Context context) {
        String query = context.getOriginalQuestion();
        if (query == null || query.isEmpty()) return;

        // Splitting the query
        String[] queryTerms = query.toLowerCase().split("\\W+");
        // Adding terms to Context
        if (context.getQueryTerms() == null || context.getQueryTerms().isEmpty()) {
            context.setQueryTerms(Arrays.asList(queryTerms));
        }

        //Scoring (Keyword Search)
        Map<Chunk, Double> scores = new HashMap<>();
        for (String term : queryTerms) {
            if (term.isEmpty()) continue;
            
            // Find chunks from index
            Map<Chunk, Integer> matches = index.search(term);
            
            for (Map.Entry<Chunk, Integer> entry : matches.entrySet()) {
                Chunk chunk = entry.getKey();
                int tf = entry.getValue();
                scores.put(chunk, scores.getOrDefault(chunk, 0.0) + tf);
            }
        }

        // Order according to score
        List<Map.Entry<Chunk, Double>> sortedEntries = new ArrayList<>(scores.entrySet());
        sortedEntries.sort((e1, e2) -> Double.compare(e2.getValue(), e1.getValue())); // Decreasing

        // Take first K term
        if (sortedEntries.size() > k) {
            sortedEntries = sortedEntries.subList(0, k);
        }

        //Chunk -> Map<String, String>
        List<Hit> retrievalHits = new ArrayList<>();

        for (Map.Entry<Chunk, Double> entry : sortedEntries) {
            Chunk chunk = entry.getKey();
            Double score = entry.getValue();

            Map<String, String> hitMap = new HashMap<>();
            hitMap.put("id", chunk.getId());
            
            String documentId = (chunk.getId() != null) ? chunk.getId() : chunk.getId();
            hitMap.put("docId", documentId);
            
            hitMap.put("text", chunk.getText());
            hitMap.put("score", String.valueOf(score)); 

            try {
                hitMap.put("json", chunk.toJson());
            } catch (Exception e) {
                
            }
            
            
            retrievalHits.add(new Hit(chunk,score));
        }

        // Update Context
        context.setRetrievalHits(retrievalHits);
        System.out.println("   -> Retriever " + retrievalHits.size() + " sonuç buldu ve Context'e işledi.");
    }

    @Override
    public String getName() {
        return "SimpleRetriever";
    }
}
