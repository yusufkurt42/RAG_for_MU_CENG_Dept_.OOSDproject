package com.cse3063.rag.parser;

import org.apache.tika.Tika;
import org.apache.tika.exception.TikaException;

import java.io.IOException;
import java.nio.file.Path;

public class DocumentParser implements IDocumentParser {

    private final Tika tika;

    public DocumentParser() {
        this.tika = new Tika();
    }

    @Override
    public String parseFileToText(Path filePath) {
        try {
            return tika.parseToString(filePath);
        } catch (IOException | TikaException e) {
            System.err.println("An error occured: " + filePath.toString());
            e.printStackTrace();
            return "";
        }
    }
}
