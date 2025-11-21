package com.cse3063.rag.normalizer;

public interface ITextNormalizer {
    
    /**
     * @param String.
     * @return normalized String
     */
    String normalize(String rawString);
    
}