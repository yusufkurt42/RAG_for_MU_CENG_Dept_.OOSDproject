package com.cse3063.rag.rerank;

import com.cse3063.rag.PipelineStage;
import com.cse3063.rag.RagContext;
import java.util.*;

public class PhraseAwareReranker implements PipelineStage {

    private final int topK;
    private final double PHRASE_BONUS = 2.0;

    public PhraseAwareReranker(int topK) {
        this.topK = topK;
    }

    @Override
    public RagContext execute(RagContext context) {

        //Take Map List from context
        List<Map<String, String>> hits = context.getRetrievalHits();

        if (hits == null || hits.isEmpty()) {
            return context;
        }

        String query = context.getOriginalQuestion().toLowerCase().trim();

        //Look at list and update scores
        for (Map<String, String> hitMap : hits) {
            //Take strings from map
            String text = hitMap.getOrDefault("text", "").toLowerCase();
            String scoreStr = hitMap.getOrDefault("score", "0.0");

            // Convert to double
            double currentScore = 0.0;
            try {
                currentScore = Double.parseDouble(scoreStr);
            } catch (NumberFormatException e) {
                currentScore = 0.0;
            }

            //If there is full matching, add score
            if (text.contains(query)) {
                currentScore += PHRASE_BONUS;
            }

            //Write new score to Map
            hitMap.put("score", String.valueOf(currentScore));
        }

        //Order list by new score
        hits.sort((map1, map2) -> {
            double s1 = Double.parseDouble(map1.get("score"));
            double s2 = Double.parseDouble(map2.get("score"));
            return Double.compare(s2, s1); // decreasing order
        });

        //Keep only first K elements
        if (hits.size() > topK) {
            //It makes a new Arraylist from subList
            hits = new ArrayList<>(hits.subList(0, topK));
        }

        //Put updated list to Context
        context.setRetrievalHits(hits);
        return context;
    }

	@Override
	public String getName() {
		// TODO Auto-generated method stub
		return null;
	}
}