package com.cse3063.rag.answer;

import com.cse3063.rag.model.Chunk;
import com.cse3063.rag.model.ChunkStore;
import com.cse3063.rag.orchestrator.Context;
import com.cse3063.rag.retriever.Hit;
import com.cse3063.rag.store.JsonChunkStore;


import java.util.Comparator;
import java.util.List;

/**
 * Adapter implementation that makes the existing answering logic usable as a PipelineStage.
 */
public class TemplateAnswerAgent implements AnswerAgent{

    private final ChunkStore store; // lightweight dependency for fetching chunks
	
	public TemplateAnswerAgent(ChunkStore store) {
        this.store = store;
    }

    @Override
    public void execute(Context context) {
        // Extract state
        List<String> query = context.getQueryTerms();
        List<Hit> topHits = context.getRetrievalHits();

        Answer answer = answer(query, topHits);
        context.setFinalAnswer(answer);
    }

    public Answer answer(List<String> query, List<Hit> topHits) {
        if (topHits == null || topHits.isEmpty()) {
            return new Answer("Üzgünüz, sorunuzla ilgili yeterli bilgi bulunamadı.", List.of());
        }

        // Get best hit
        Hit bestHit = topHits.get(0);
        Chunk bestHitChunk = bestHit.getChunk();
        if (bestHitChunk == null) {
            return new Answer("Kaynak metin bulunamadı, indeks hatası.", List.of());
        }
        
        //Get the sentences in our chunk
        String chunkContent = bestHitChunk.getText();
        List<String> sentences = List.of(chunkContent.split("[\\.\\?\\!]"));
        
        // get the answer sentence using streams
        String answerSentence = sentences.stream()
                .map(String::trim)
                .filter(s -> !s.isEmpty())
                .max(Comparator.comparingLong(sentence -> 
                    query.stream()
                          .filter(term -> sentence.toLowerCase().contains(term))
                          .count()
                ))
                .orElse(sentences.get(0));//return first sentence if no match
        
        

        // create the citations, in first iteration we have only one citation
        String citation = String.format("%s:%s:%d-%d", bestHitChunk.getDocId(), bestHitChunk.getId(), bestHitChunk.getStartOffset(), bestHitChunk.getEndOffset());
        List<String> citations = List.of(citation);

        // Create the answer, "Your answer: {bestSentence}. See: {citation}"
        String finalAnswerText = String.format("Your answer: %s. See: %s", answerSentence, citation);
        Answer finalAnswer = new Answer(finalAnswerText, citations);
        
        return finalAnswer;
    }

    @Override
    public String getName() {
        return "answer_agent";
    }
}
