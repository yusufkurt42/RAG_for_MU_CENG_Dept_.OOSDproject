package com.cse3063.rag.model;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;

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

    /**
     * Depodaki tüm Chunk nesnelerini bir liste olarak döndürür.
     * Index oluşturma veya toplu işlemler için kullanılır.
     * @return Tüm Chunk'ların listesi.
     */
    public List<Chunk> getAllChunks() {
        // Map'in değerlerini (Values) yeni bir ArrayList'e dönüştürerek döndürür.
        return new ArrayList<>(chunkMap.values());
    }
}