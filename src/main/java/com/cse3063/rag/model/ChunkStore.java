package com.cse3063.rag.model;

import java.util.Map;
import java.util.Collections;

public class ChunkStore {
    // Chunk ID'ye göre hızlı erişim sağlayan harita.
    private final Map<String, Chunk> chunkMap;

    public ChunkStore(Map<String, Chunk> chunkMap) {
        this.chunkMap = Collections.unmodifiableMap(chunkMap); // Dışarıdan değiştirilemez yap
    }

    /**
     * Chunk ID'sine göre Chunk nesnesini döndürür.
     * @param chunkId Aranacak Chunk'ın ID'si.
     * @return Bulunan Chunk nesnesi veya yoksa null.
     */
    public Chunk getChunk(String chunkId) {
        return chunkMap.get(chunkId);
    }
    
    // Diğer yardımcı metotlar (örneğin tüm ID'leri listeleme) buraya eklenebilir.
}