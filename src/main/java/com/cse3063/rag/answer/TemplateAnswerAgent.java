package com.cse3063.rag.answer;

import com.cse3063.rag.orchestrator.Context;
import com.cse3063.rag.retriever.Hit;
import com.cse3063.rag.store.JsonChunkStore;
import java.util.List;

/**
 * Adapter implementation that makes the existing answering logic usable as a PipelineStage.
 */
public class TemplateAnswerAgent implements AnswerAgent{

    private final JsonChunkStore store; // lightweight dependency for fetching chunks

    public TemplateAnswerAgent() {
        this.store = new JsonChunkStore();
    }

    @Override
    public void execute(Context context) {
        // Extract state
        List<String> query = context.getQueryTerms();
        List<Hit> topHits = context.getRetrievalHits();

        Answer answer = buildAnswer(query, topHits, store);
        context.setFinalAnswer(answer);
    }

    // Refactored answering logic into a helper that returns an Answer
    private Answer buildAnswer(List<String> query, List<Hit> topHits, JsonChunkStore store) {
        if (topHits == null || topHits.isEmpty()) {
            return new Answer("Üzgünüz, sorunuzla ilgili yeterli bilgi bulunamadı.", List.of());
        }

        // For now, we'll produce a simple answer using the first hit.
        Hit bestHit = topHits.get(0);
        // NOTE: JsonChunkStore currently doesn't provide a getChunk method; this is a placeholder.
        // In a real implementation you'd look up the chunk content by ID here.
        String finalAnswerText = String.format("Your answer: (content from best hit id=%s)", bestHit.getChunk().getId());
        return new Answer(finalAnswerText, List.of());
    }

    @Override
    public String getName() {
        return "answer_agent";
    }
}
