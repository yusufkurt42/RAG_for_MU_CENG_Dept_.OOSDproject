package com.cse3063.rag.tracer;

import java.util.ArrayList;
import java.util.List;

public class TraceBus {
    
    // That holds the list of subscribers (SOLID: Open/Closed - New sink types can be added)
    private List<TraceSink> observers = new ArrayList<>();

    //Add subscriber
    public void register(TraceSink sink) {
        this.observers.add(sink);
    }

    //  Event to all subscribers
    public void trace(TraceEvent event) {
        for (TraceSink sink : observers) {
            sink.log(event);
        }
    }
    
    //  (Close all sinks)
    public void closeAll() {
        for (TraceSink sink : observers) {
            sink.close();
        }
    }
}
