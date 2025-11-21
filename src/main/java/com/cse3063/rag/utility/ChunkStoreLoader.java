package com.cse3063.rag.utility;

import com.cse3063.rag.model.Chunk;
import com.cse3063.rag.model.ChunkStore;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class ChunkStoreLoader {

    /**
     * JSON dosyasından tüm Chunk'ları okur ve bir ChunkStore oluşturur.
     * * Proje gereksinimi: Chunk'lar dosyada bir List<Chunk> olarak saklanmalıdır.
     *
     * @param chunkPath Chunk verilerinin JSON dosya yolu.
     * @return Yüklü Chunk'ları içeren yeni bir ChunkStore nesnesi.
     * @throws RuntimeException I/O veya JSON ayrıştırma hatası durumunda.
     */
    public static ChunkStore load(String chunkPath) {
        
        File file = new File(chunkPath);
        if (!file.exists()) {
            throw new RuntimeException("Chunk data file not found at path: " + chunkPath);
        }

        ObjectMapper mapper = new ObjectMapper();
        List<Chunk> chunkList;
        
        try {
            // 1. JSON dosyasını List<Chunk> yapısına dönüştürür.
            chunkList = mapper.readValue(file, new TypeReference<List<Chunk>>() {});
            
        } catch (IOException e) {
            // Dosya okuma veya JSON format hatası
            throw new RuntimeException("Failed to read or parse chunk data from " + chunkPath + ": " + e.getMessage(), e);
        }

        // 2. List<Chunk>'ı, ChunkStore'un beklediği Map<ID, Chunk> yapısına dönüştürür.
        Map<String, Chunk> chunkMap = chunkList.stream()
            .collect(Collectors.toMap(
                Chunk::getId, // Key: Chunk ID
                chunk -> chunk  // Value: Chunk nesnesinin kendisi
            ));

        // 3. ChunkStore'u oluştur ve döndür.
        return new ChunkStore(chunkMap);
    }
}