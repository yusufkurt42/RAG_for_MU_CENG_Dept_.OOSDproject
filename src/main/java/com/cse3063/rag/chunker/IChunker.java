package com.cse3063.rag.chunker;

import com.cse3063.rag.model.Chunk;
import java.util.List;

public interface IChunker {
    /**
     * @param 
     * @param 
     * @return 
     */
    List<Chunk> chunk(String docId, String fullText);
}