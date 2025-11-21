package com.cse3063.rag.orchestrator;

public class RagApplication {

    public static void main(String[] args) {
        // Varsayılan Değerler (Fallback)
        String configPath = "src/main/resources/config.json";
        String chunkPath = "src/main/resources/chunks.json"; // Genelde config içinden okunur ama parametre de olabilir
        String question = "Ali Haydar Özer'in maili nedir?"; // Varsayılan test sorusu

        // 1. CLI Argümanlarını Ayrıştır (Basit Parsing)
        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "--config":
                    if (i + 1 < args.length) configPath = args[++i];
                    break;
                case "--chunks": // Opsiyonel: Chunk path'i dışarıdan vermek isterseniz
                    if (i + 1 < args.length) chunkPath = args[++i];
                    break;
                case "--q":
                case "--question":
                    if (i + 1 < args.length) question = args[++i];
                    break;
            }
        }

        System.out.println("Başlatılıyor...");
        System.out.println("Config: " + configPath);
        System.out.println("Soru: " + question);

        try {
            // 2. Controller'ı Başlat (Orkestratör)
            // Not: Chunk path genelde config dosyasının içinde "data_paths" altında tanımlıdır.
            // Ancak constructor'ınız ayrı istiyorsa böyle kalabilir.
            RagOrchestrator orchestrator = new RagOrchestrator(configPath, chunkPath);

            // 3. Senaryoyu Çalıştır
            String answer = orchestrator.answerQuestion(question);

            // 4. Çıktıyı Yazdır (stdout: final answer line) [cite: 151]
            System.out.println("\n" + answer);

        } catch (Exception e) {
            System.err.println("Uygulama Hatası: " + e.getMessage());
            e.printStackTrace();
        }
    }
}