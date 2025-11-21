package com.cse3063.rag.store;

import com.cse3063.rag.model.Chunk;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;

public class JsonChunkStore {

    public void saveChunksToFile(List<Chunk> chunks, String filePath) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filePath))) {
            
            writer.write("[\n"); 

            for (int i = 0; i < chunks.size(); i++) {
                Chunk chunk = chunks.get(i);
                
                writer.write("  " + chunk.toJson());

                if (i < chunks.size() - 1) {
                    writer.write(",\n");
                } else {
                    writer.write("\n");
                }
            }

            writer.write("]"); 
            
            System.out.println("Chunks saved successfully: " + filePath);

        } catch (IOException e) {
            System.err.println("An error occurred while writing the file: " + e.getMessage());
        }
    }
}