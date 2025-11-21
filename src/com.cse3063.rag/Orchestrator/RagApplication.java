import java.util.HashMap;
import java.util.Map;

public class RagApplication {
    public static void main(String[] args) {
        // 1. Load Configuration (Simulated primitive loading)
        // In reality, this comes from your JSON/YAML parser
        Map<String, Object> mockConfig = new HashMap<>();
        mockConfig.put("log_level", "DEBUG");

        // 2. Initialize Controller
        RagOrchestrator orchestrator = new RagOrchestrator(mockConfig);

        // 3. Run Scenario
        String question = "What is Dr. Ganiz's office?";
        String answer = orchestrator.answerQuestion(question);

        // 4. Output
        System.out.println("\nFinal Result:\n" + answer);
    }
}