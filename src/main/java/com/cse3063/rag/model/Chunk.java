package com.cse3063.rag.model;

public class Chunk {
    private String id;         
    private String docId;      
    private String text;        
    private int startOffset;  
    private int endOffset;     

    public Chunk(String id, String docId, String text, int startOffset, int endOffset) {
        this.id = id;
        this.docId = docId;
        this.text = text;
        this.startOffset = startOffset;
        this.endOffset = endOffset;
    }

    public String getId() { return id; }
    public String getText() { return text; }
    
    public String toJson() {
        return String.format(
            "{\"id\": \"%s\", \"docId\": \"%s\", \"startOffset\": %d, \"endOffset\": %d, \"text\": \"%s\"}",
            id, docId, startOffset, endOffset, escapeJson(text)
        );
    }

    public String getDocId() {
        return docId;
    }

    public int getStartOffset() {
        return startOffset;
    }

    public int getEndOffset() {
        return endOffset;
    }

    private String escapeJson(String str) {
        return str.replace("\"", "\\\"").replace("\n", "\\n");
    }
}