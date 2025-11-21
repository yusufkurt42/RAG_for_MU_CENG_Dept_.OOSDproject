package com.cse3063.rag.reranker;

import com.cse3063.rag.orchestrator.PipelineStage;
import com.cse3063.rag.orchestrator.Context;
import com.cse3063.rag.retriever.Hit;
import java.util.Comparator;
import java.util.List;

public class PhraseAwareReranker implements Reranker {

    private static final double PHRASE_BOOST = 5.0; // Configurable boost value

    @Override
    public void execute(Context context) {
        String query = context.getOriginalQuestion();
        List<Hit> hits = context.getRetrievalHits();

        if (query == null || query.isEmpty() || hits == null || hits.isEmpty()) {
            return;
        }

        String lowerQuery = query.toLowerCase().trim();

        // 1. Re-score: Check if the exact query phrase appears in the text
        for (Hit hit : hits) {
            if (hit.getChunk().getText() != null) {
                String lowerText = hit.getChunk().getText().toLowerCase();
                if (lowerText.contains(lowerQuery)) {
                    // Apply boost to the existing score
                    double newScore = hit.getInitialScore() + PHRASE_BOOST;
                    hit.setRerankScore(newScore);
                }
            }
        }

        // 2. Re-sort: Order by new scores (Descending)
        hits.sort(Comparator.comparingDouble(Hit::getRerankScore).reversed());

        // 3. Update Context
        context.setRetrievalHits(hits);
        System.out.println("   -> PhraseAwareReranker re-sorted " + hits.size() + " hits.");
        return;
    }

    @Override
    public String getName() {
        return "PhraseAwareReranker";
    }
}