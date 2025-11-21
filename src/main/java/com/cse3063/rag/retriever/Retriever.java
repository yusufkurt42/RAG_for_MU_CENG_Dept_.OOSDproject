package com.cse3063.rag.retriever;

import com.cse3063.rag.orchestrator.Context;
import com.cse3063.rag.orchestrator.PipelineStage;

public interface Retriever extends PipelineStage{
    // Inherits Context execute(Context) from PipelineStage
}