package com.example;

public interface TraceSink {
    void log(TraceEvent event);
    void close(); // For closing the file
}
