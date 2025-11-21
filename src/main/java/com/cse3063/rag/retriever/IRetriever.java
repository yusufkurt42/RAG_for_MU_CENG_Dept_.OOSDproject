package com.cse3063.rag.retriever;

import com.cse3063.rag.orchestrator.Context;

public interface IRetriever {
    void execute(Context context);
}