package com.cse3063.rag.orchestrator;

import com.cse3063.rag.detector.Intent;
import com.cse3063.rag.detector.IntentDetector;
import com.cse3063.rag.detector.RuleIntentDetector;
import com.cse3063.rag.model.ChunkStore;
import com.cse3063.rag.retriever.KeywordIndex;
import com.cse3063.rag.retriever.Retriever;
import com.cse3063.rag.retriever.SimpleRetriever;
import com.cse3063.rag.answer.AnswerAgent;
import com.cse3063.rag.answer.TemplateAnswerAgent;
import com.cse3063.rag.store.JsonChunkStore;
import com.cse3063.rag.utility.ChunkStoreLoader;
import com.cse3063.rag.utility.JsonConfigLoader;
import com.cse3063.rag.writer.HeuristicQueryWriter;
import com.cse3063.rag.writer.QueryWriter;
import com.cse3063.rag.reranker.Reranker;
import com.cse3063.rag.reranker.PhraseAwareReranker;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;

public class ComponentFactory {

    @SuppressWarnings("unchecked")
    private static Map<String, Object> getConfigSection(Map<String, Object> masterConfig, String sectionKey) {
        if (!masterConfig.containsKey(sectionKey)) {
            throw new IllegalArgumentException("Master config is missing section: " + sectionKey);
        }
        return (Map<String, Object>) masterConfig.get(sectionKey);
    }


    public static ChunkStore createChunkStore(String configPath) throws IOException {
        
        // 1. Load the master configuration map.
        Map<String, Object> masterConfig = JsonConfigLoader.loadAndParse(configPath);
        
        // 2. Extract the section that contains file paths. (Assuming "data_paths" key)
        Map<String, Object> dataConfig = getConfigSection(masterConfig, "data_paths");
        
        // 3. Extract the specific chunk file path.
        String chunkPath = (String) dataConfig.get("chunk_file_path");

        if (chunkPath == null || chunkPath.isEmpty()) {
            throw new IllegalArgumentException("Config error: 'chunk_file_path' is missing in 'data_paths' section.");
        }
        
        // 4. Call the dedicated loader to read the file and build the ChunkStore map.
        return ChunkStoreLoader.load(chunkPath);
    }


    /**
     * Creates the IntentDetector strategy by reading the master configuration file.
     * The factory handles the file I/O internally.
     * @throws IOException 
     */
    public static IntentDetector createIntentDetector(String configPath) throws IOException {// 1. Load the master configuration from the path
        Map<String, Object> masterConfig = JsonConfigLoader.loadAndParse(configPath);
        
        // 2. Extract the specific Intent Detector section
        Map<String, Object> config = getConfigSection(masterConfig, "intent_detector");
        String type = (String) Optional.ofNullable(config.get("type")).orElse("rule");

        if (!type.equalsIgnoreCase("rule")) {
            throw new IllegalArgumentException("Unsupported IntentDetector type: " + type);
        }

        // --- 3. Extract Intent Rules (Map<Intent, List<String>>) ---
        Map<Intent, List<String>> intentRules;
        Object rulesObject = config.get("rules"); // Assumed key in config file
        
        if (rulesObject instanceof Map) {
            Map<String, List<String>> rawRules = (Map<String, List<String>>) rulesObject;
            
            // Convert String Keys to Intent Enum Keys
            intentRules = rawRules.entrySet().stream()
                .collect(Collectors.toMap(
                    entry -> Intent.valueOf(entry.getKey().toUpperCase()), 
                    Map.Entry::getValue
                ));
        } else {
            throw new IllegalStateException("Config error: 'rules' field is missing or not a Map.");
        }
        
        // --- 4. Extract Priority Array (int[]) ---
        int[] priorityArray = new int[0];
        Object priorityObject = config.get("priority"); // Assumed key in config file

        if (priorityObject instanceof List) {
            // Safely cast List<Number> to int[]
            List<?> priorityList = (List<?>) priorityObject;
            
            priorityArray = priorityList.stream()
                .map(n -> ((Number)n).intValue()) // Cast Number types to Integer
                .mapToInt(Integer::intValue)
                .toArray();
        } 
        
        // 5. Instantiate the RuleIntentDetector with the two mandatory parameters
        return new RuleIntentDetector(intentRules, priorityArray);
    }

    /**
     * Creates the QueryWriter strategy by reading the master configuration file.
     * @throws IOException 
     */
    public static QueryWriter createQueryWriter(String configPath) throws IOException {
        // 1. Load the master configuration from the path
        Map<String, Object> masterConfig = JsonConfigLoader.loadAndParse(configPath);
        
        // 2. Extract the specific QueryWriter section
        Map<String, Object> config = getConfigSection(masterConfig, "query_writer");
        String type = (String) Optional.ofNullable(config.get("type")).orElse("heuristic");

        if (!type.equalsIgnoreCase("heuristic")) {
            throw new IllegalArgumentException("Unsupported QueryWriter type: " + type);
        }

        // --- FIX: Safely Extracting Constructor Parameters ---
        
        // 3. Extract Stopwords (Casting dynamic list to List<String>)
        List<String> stopwords;
        if (config.get("stopwords") instanceof List) {
            stopwords = (List<String>) config.get("stopwords");
        } else {
            throw new IllegalStateException("Config error: 'stopwords' field is missing or not a List.");
        }

        // 4. Extract Suffix List (Casting dynamic list to List<String>)
        List<String> suffixList;
        if (config.get("suffix_list") instanceof List) {
            suffixList = (List<String>) config.get("suffix_list");
        } else {
            // Must provide a default if it's optional
            suffixList = new ArrayList<>(); 
        }
        
        // 5. Extract Boosters Map (Casting complex map structure)
        // JSON libraries often read maps as Map<String, Object>
        Map<Intent, List<String>> boosters;
        if (config.get("boosters") instanceof Map) {
            Map<String, List<String>> rawBoosters = (Map<String, List<String>>) config.get("boosters");
            
            // Convert Map<String (Intent Name), List<String>> to Map<Intent, List<String>>
            boosters = rawBoosters.entrySet().stream()
                .collect(Collectors.toMap(
                    entry -> Intent.valueOf(entry.getKey().toUpperCase()), // Convert String to Intent Enum
                    Map.Entry::getValue
                ));
        } else {
            throw new IllegalStateException("Config error: 'boosters' field is missing or not a Map.");
        }
               
        
         // 6. NEW FIX: Extract Max Terms (Using default 10 if missing)
        int maxTerms = 10;
        Object maxTermsObject = config.get("max_terms");
        if (maxTermsObject instanceof Integer) {
            maxTerms = (Integer) maxTermsObject;
        } else if (maxTermsObject instanceof Long) {
             // Handle Long cast if JSON parser defaults to Long for numbers
            maxTerms = ((Long) maxTermsObject).intValue(); 
        } 
        
        // 7. Instantiate the HeuristicQueryWriter with ALL four strongly-typed parameters
        return new HeuristicQueryWriter(stopwords, boosters, suffixList, maxTerms);
    }

    /**
     * Creates the Retriever strategy. Needs external Index object (Information Expert).
     * @throws IOException 
     */
    public static Retriever createRetriever(String configPath, KeywordIndex keywordIndex) throws IOException {
        
        // 1. Konfigürasyonu Yükle
        Map<String, Object> masterConfig = JsonConfigLoader.loadAndParse(configPath);
        Map<String, Object> config = getConfigSection(masterConfig, "retriever");
        String type = (String) Optional.ofNullable(config.get("type")).orElse("simple");

        if (!type.equalsIgnoreCase("simple")) {
            throw new IllegalArgumentException("Unknown Retriever type: " + type);
        }
        
        // 2. K değerini Konfigürasyondan Çıkar
        int k = 10; // Varsayılan değer
        Object kObject = config.get("k");

        if (kObject instanceof Number) {
            k = ((Number) kObject).intValue();
        } else {
            // Konfigürasyonda yoksa veya hatalıysa uyarı verilebilir, varsayılan kullanılır.
            System.err.println("UYARI: Retriever için 'k' değeri konfigürasyonda bulunamadı, varsayılan 10 kullanılıyor.");
        }

        // 3. SimpleRetriever'ı iki zorunlu parametre ile oluştur
        return new SimpleRetriever(keywordIndex, k);
    }

    /**
     * Creates the Reranker strategy, supporting 'simple' and 'noop'.
     * @throws IOException 
     */
    public static Reranker createReranker(String configPath) throws IOException {
        Map<String, Object> masterConfig = JsonConfigLoader.loadAndParse(configPath);
        Map<String, Object> config = getConfigSection(masterConfig, "reranker");
        String type = (String) Optional.ofNullable(config.get("type")).orElse("noop"); 

        switch (type.toLowerCase()) {
            case "simple":
                return new PhraseAwareReranker();
            default:
                throw new IllegalArgumentException("Unknown Reranker type: " + type);
        }
    }

    /**
     * Creates the AnswerAgent strategy. Needs external ChunkStore and Validator.
     * @throws IOException 
     */
    public static AnswerAgent createAnswerAgent(String configPath, String chunkPath) throws IOException {
        Map<String, Object> masterConfig = JsonConfigLoader.loadAndParse(configPath);
        Map<String, Object> config = getConfigSection(masterConfig, "answer_agent");
        String type = (String) Optional.ofNullable(config.get("type")).orElse("template");

        ChunkStore store = ChunkStoreLoader.load(chunkPath);

        switch (type.toLowerCase()) {
            case "template":
                return new TemplateAnswerAgent(store);
            default:
                throw new IllegalArgumentException("Unknown AnswerAgent type: " + type);
        }
    }
}