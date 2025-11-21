package com.example;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import static org.junit.jupiter.api.Assertions.*;

class RuleIntentDetectorTest {

    private RuleIntentDetector detector;
    private final String TEST_CONFIG_PATH = "rules_test.json";
    private final int[] DEFAULT_PRIORITY = {0, 1, 2, 3, 4}; // STAFF(0) > REGISTRATION(1)...

    @BeforeEach
    void setUp() throws IOException {
        String jsonContent = "{\n" +
                "  \"STAFF_LOOKUP\": [\"hoca\", \"ofis\", \"mail\"],\n" +
                "  \"REGISTRATION\": [\"kayıt\", \"ders seçimi\"],\n" +
                "  \"POLICY_FAQ\": [\"yönetmelik\", \"sınav hakkı\"]\n" +
                "}";
        
        try (FileWriter writer = new FileWriter(TEST_CONFIG_PATH)) {
            writer.write(jsonContent);
        }
        detector = new RuleIntentDetector(TEST_CONFIG_PATH);
    }

    @AfterEach
    void tearDown() {
        new File(TEST_CONFIG_PATH).delete();
    }

    @Test
    void testIntentDetectionLogic() {
        assertEquals(Intent.STAFF_LOOKUP, detector.detect("Murat hocanın ofisi nerede?", DEFAULT_PRIORITY),"İçinde 'ofis' geçen cümle STAFF_LOOKUP dönmelidir.");

        assertEquals(Intent.REGISTRATION, detector.detect("Ders seçimi ne zaman?", DEFAULT_PRIORITY),"İçinde 'ders seçimi' geçen cümle REGISTRATION dönmelidir.");

        assertEquals(Intent.STAFF_LOOKUP, detector.detect("Hoca kayıt onayı veriyor mu?", DEFAULT_PRIORITY),"Çakışma durumunda priority listesine göre STAFF seçilmelidir.");

        assertEquals(Intent.UNKNOWN, detector.detect("Hava durumu nasıl?", DEFAULT_PRIORITY),"Tanımlı keyword içermeyen cümle UNKNOWN dönmelidir.");
    }
    /* This test class ensures/verifies that:

The RuleIntentDetector class correctly reads the JSON configuration file.

Simple keyword matching is performed correctly.

The priority order is respected when a sentence contains multiple intents.

The system returns UNKNOWN gracefully instead of crashing in undefined scenarios. */ 
}