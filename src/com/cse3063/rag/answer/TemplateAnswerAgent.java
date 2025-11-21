import java.util.Comparator;
import java.util.List;

public class TemplateAnswerAgent implements AnswerAgent , PipelineStage{

    public TemplateAnswerAgent() {
    }

    public Answer answer(List<String> query, List<Hit> topHits, ChunkStore store) {
        if (topHits == null || topHits.isEmpty()) {
            return new Answer("Üzgünüz, sorunuzla ilgili yeterli bilgi bulunamadı.", List.of());
        }

        // Get best hit
        Hit bestHit = topHits.get(0);
        Chunk bestHitChunk = store.getChunk(bestHit.getChunkId());
        if (bestHitChunk == null) {
            return new Answer("Kaynak metin bulunamadı, indeks hatası.", List.of());
        }
        
        //Get the sentences in our chunk
        String chunkContent = bestHitChunk.getContent();
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
        String citation = String.format("%s:%s:%d-%d", bestHitChunk.getDocId(), bestHitChunk.getSectionId(), bestHitChunk.getStartOffset(), bestHitChunk.getEndOffset());
        List<String> citations = List.of(citation);

        // Create the answer, "Your answer: {bestSentence}. See: {citation}"
        String finalAnswerText = String.format("Your answer: %s. See: %s", answerSentence, citation);
        Answer finalAnswer = new Answer(finalAnswerText, citations);
        
        return finalAnswer;
    }
	
}
