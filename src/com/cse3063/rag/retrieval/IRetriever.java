package com.cse3063.rag.retrieval;

import java.util.List;

public interface IRetriever {
    List<Hit> retrieve(String query, int k);
}