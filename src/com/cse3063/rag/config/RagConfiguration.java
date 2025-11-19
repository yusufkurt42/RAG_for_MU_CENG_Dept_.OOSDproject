package com.cse3063.rag.config;

public class RagConfiguration {
    
    private int windowSize = 400;
    private int overlap = 50;
    private String inputFilePath = "Bilimsel_Etkinlik_Katilimi_Dilekce.pdf";
    private String outputFilePath = "SourceCollection&Chunking/chunks.json";

    public int getWindowSize() {
        return windowSize;
    }

    public int getOverlap() {
        return overlap;
    }

    public String getInputFilePath() {
        return inputFilePath;
    }

    public String getOutputFilePath() {
        return outputFilePath;
    }
    
}