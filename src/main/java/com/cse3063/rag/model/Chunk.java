package com.cse3063.rag.model;

import com.fasterxml.jackson.annotation.JsonProperty; // İsteğe bağlı: Alan adlarını garantilemek için

public class Chunk {
    private String id;
    private String docId;
    private int startOffset;
    private int endOffset;
    private String text;

    // 1. Jackson İçin Zorunlu: Parametresiz (Boş) Constructor
    public Chunk() {
    }

    // Tüm alanları alan Constructor
    public Chunk(String id, String docId, int startOffset, int endOffset, String text) {
        this.id = id;
        this.docId = docId;
        this.startOffset = startOffset;
        this.endOffset = endOffset;
        this.text = text;
    }

    // --- Getters ---
    public String getId() { return id; }
    public String getDocId() { return docId; }
    public int getStartOffset() { return startOffset; }
    public int getEndOffset() { return endOffset; }
    public String getText() { return text; }

    // --- Setters (Jackson'ın veriyi yazması için gereklidir) ---
    public void setId(String id) { this.id = id; }
    public void setDocId(String docId) { this.docId = docId; }
    public void setStartOffset(int startOffset) { this.startOffset = startOffset; }
    public void setEndOffset(int endOffset) { this.endOffset = endOffset; }
    public void setText(String text) { this.text = text; }

    // JSON String Formatı (Manuel oluşturma için)
    public String toJson() {
        return String.format(
            "{\"id\": \"%s\", \"docId\": \"%s\", \"startOffset\": %d, \"endOffset\": %d, \"text\": \"%s\"}",
            id, docId, startOffset, endOffset, escapeJson(text)
        );
    }

    private String escapeJson(String str) {
        if (str == null) return "";
        return str.replace("\"", "\\\"").replace("\n", "\\n");
    }
}