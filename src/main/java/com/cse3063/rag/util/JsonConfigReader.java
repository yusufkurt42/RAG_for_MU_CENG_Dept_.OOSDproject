package com.cse3063.rag.util;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.util.Map;

/**
 * JsonConfigReader: Handles file I/O and JSON parsing for the application configuration.
 * This implementation relies on the Jackson library.
 */
public class JsonConfigReader {

    /**
     * Reads the configuration file from the specified path and parses it into a Map.
     * * @param configPath The file path to the master configuration file (JSON/YAML).
     * @return A Map<String, Object> representing the entire configuration structure.
     * @throws IOException If the file is not found, cannot be read, or parsing fails.
     */
    public static Map<String, Object> loadMasterConfig(String configPath) throws IOException {
        
        if (configPath == null || configPath.trim().isEmpty()) {
            throw new IllegalArgumentException("Configuration path cannot be null or empty.");
        }
        
        File configFile = new File(configPath);
        
        if (!configFile.exists()) {
            throw new IOException("Configuration file not found at path: " + configPath);
        }
        
        // ObjectMapper is the central object for JSON serialization/deserialization in Jackson.
        ObjectMapper mapper = new ObjectMapper();
        
        // We use a TypeReference to inform Jackson to deserialize the file content 
        // directly into a Map<String, Object> structure, which is generic 
        // enough for the RagFactory to use.
        
        try {
            return mapper.readValue(configFile, new TypeReference<Map<String, Object>>() {});
        } catch (IOException e) {
            // Catches parsing errors (malformed JSON/YAML) or file read errors
            throw new IOException("Error processing configuration file " + configPath + ": " + e.getMessage(), e);
        }
    }
}