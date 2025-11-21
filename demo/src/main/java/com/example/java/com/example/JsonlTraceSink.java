package com.example;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class JsonlTraceSink implements TraceSink {

    private BufferedWriter writer;
    private ObjectMapper objectMapper;

    public JsonlTraceSink() {
        this.objectMapper = new ObjectMapper();
        // For making appropriate Date format
        this.objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        setupFile();
    }

    private void setupFile() {
        try {
            // 1. logs klasörünü oluştur
            File directory = new File("logs");
            if (!directory.exists()) {
                directory.mkdirs();
            }

            // 2. Dosya adını oluştur (run-YYYYMMDD-HHMMSS.jsonl)
            String timeStamp = new SimpleDateFormat("yyyyMMdd-HHmmss").format(new Date());
            String fileName = "logs/run-" + timeStamp + ".jsonl";

            // 3. Writer'ı başlat (append: true)
            this.writer = new BufferedWriter(new FileWriter(fileName, true));
            
            System.out.println("Trace log started: " + fileName);

        } catch (IOException e) {
            System.err.println("Log dosyası oluşturulamadı: " + e.getMessage());
        }
    }

    @Override
    public void log(TraceEvent event) {
        if (writer == null) return;

        try {
            //Convert event object to JSON string
            String jsonLine = objectMapper.writeValueAsString(event);
            
            //  Write the JSON line to the file and move to a new line (JSONL format).
            writer.write(jsonLine);
            writer.newLine();
            writer.flush(); //Every line is saved so that data is not lost even if the program crashes.
            
        } catch (IOException e) {
            System.err.println("Log yazma hatası: " + e.getMessage());
        }
    }

    @Override
    public void close() {
        try {
            if (writer != null) writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
