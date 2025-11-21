package com.cse3063.rag.tracer;

public interface TraceSink {
    void log(TraceEvent event);
    void close(); // For closing the file
}
