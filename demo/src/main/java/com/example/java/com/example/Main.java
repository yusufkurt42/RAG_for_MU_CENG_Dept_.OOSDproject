package com.example;

public class Main {
    public static void main(String[] args) {
            TraceBus traceBus = new TraceBus();
            JsonlTraceSink jsonSink = new JsonlTraceSink();

            traceBus.register(jsonSink);

             traceBus.trace(new TraceEvent("IntentDetection", "Hoca oda nerede?", "STAFF_LOOKUP", 10));
    }
}