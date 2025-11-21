import java.util.List;

public interface AnswerAgent {
	Answer answer(List<String> query, List<Hit> hits, ChunkStore store);
}
