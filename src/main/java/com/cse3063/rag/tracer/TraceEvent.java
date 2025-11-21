package com.cse3063.rag.tracer;

import java.time.Instant;

// This class summarizes what happens at any step of the pipeline.
public class TraceEvent {
    private String stage;          //  Example: "IntentDetection", "Retrieval"
    private Object input;          //  Example: The data entering that step (Question, Query list, etc.)
    private Object output;         //  Example: The data exiting that step (Intent, Hit list, etc.)
    private long timestamp;        //  Example: When the event occurred (Unix epoch ms)
    private long durationMs;       //  Example: How long the operation took (optional but useful)

    public TraceEvent(String stage, Object input, Object output, long durationMs) {
        this.stage = stage;
        this.input = input;
        this.output = output;
        this.timestamp = Instant.now().toEpochMilli();
        this.durationMs = durationMs;
    }

    // Getter methods (needed for Jackson to convert to JSON)
    public String getStage() { return stage; }
    public Object getInput() { return input; }
    public Object getOutput() { return output; }
    public long getTimestamp() { return timestamp; }
    public long getDurationMs() { return durationMs; }
}
