package com.cse3063.rag.parser;

import java.nio.file.Path;


public interface IDocumentParser {
    
    /**
     * @param filePath.
     * @return String of file, it returns empty String if an error occurs
     */
    String parseFileToText(Path filePath);
    
}