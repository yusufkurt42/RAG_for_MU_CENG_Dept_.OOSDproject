package com.cse3063.rag.normalizer;

public class BaseTextNormalizer implements ITextNormalizer {

    @Override
    public String normalize(String rawText) {
        if (rawText == null) {
            return "";
        }

        String lowercased = rawText.toLowerCase();
        String normalized = lowercased.replaceAll("\\p{P}", "");
        normalized = normalized.replaceAll("\\s+", " ");
        return normalized.trim();
    }
}