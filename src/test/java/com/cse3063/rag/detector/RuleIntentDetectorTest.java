package com.cse3063.rag.detector;

import com.cse3063.rag.orchestrator.Context;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class RuleIntentDetectorTest {

    private RuleIntentDetector detector;

    @BeforeEach
    void setUp() {
        // 1. Define Test Rules
        Map<Intent, List<String>> rules = Map.of(
            Intent.REGISTRATION, List.of("kayit", "ders secimi"),
            Intent.STAFF_LOOKUP, List.of("ofis", "hoca", "mail"),
            Intent.POLICY_FAQ,   List.of("yonerge", "mevzuat")
        );

        // 2. Define Priority: STAFF_LOOKUP (1) > REGISTRATION (0) > POLICY_FAQ (2)
        // Ordinals: REGISTRATION=0, STAFF_LOOKUP=1, POLICY_FAQ=2...
        int[] priority = {1, 0, 2}; 

        // 3. Instantiate Detector
        detector = new RuleIntentDetector(rules, priority);
    }

    @Test
    void testBasicKeywordMatch() {
        Context context = new Context("Yaz okulu kayit tarihleri ne zaman?");
        detector.execute(context);
        assertEquals(Intent.REGISTRATION, context.getCurrentIntent(), "Should detect REGISTRATION from 'kayit'");
    }

    @Test
    void testCaseInsensitivity() {
        Context context = new Context("HOCANIN OFIS saati kacta?"); // Upper case input
        detector.execute(context);
        assertEquals(Intent.STAFF_LOOKUP, context.getCurrentIntent(), "Should detect STAFF_LOOKUP despite uppercase input");
    }

    @Test
    void testPriorityTieBreaking() {
        // Question contains keywords for both REGISTRATION ("kayit") and STAFF_LOOKUP ("ofis")
        Context context = new Context("Kayit icin hocanin ofisine gitmem gerekir mi?");
        
        detector.execute(context);
        
        // Since STAFF_LOOKUP (1) is first in our priority array {1, 0, 2}, it should win.
        assertEquals(Intent.STAFF_LOOKUP, context.getCurrentIntent(), "Should respect priority array (STAFF > REGISTRATION)");
    }

    @Test
    void testNoMatchReturnsUnknown() {
        Context context = new Context("Hava durumu nasil?");
        detector.execute(context);
        assertEquals(Intent.UNKNOWN, context.getCurrentIntent(), "Should return UNKNOWN if no keywords match");
    }
    
    @Test
    void testEmptyQuestion() {
        Context context = new Context("");
        detector.execute(context);
        assertEquals(Intent.UNKNOWN, context.getCurrentIntent());
    }
}