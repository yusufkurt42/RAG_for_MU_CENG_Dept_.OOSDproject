package com.cse3063.rag.writer;

import com.cse3063.rag.detector.Intent;
import com.cse3063.rag.orchestrator.Context;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class HeuristicQueryWriterTest {

    private HeuristicQueryWriter writer;
    
    // Test Konfigürasyon Verileri
    private List<String> testStopwords;
    private List<String> testSuffixes;
    private Map<Intent, List<String>> testBoosters;
    private int testMaxTerms = 10;

    @BeforeEach
    void setUp() {
        // 1. Stopwords: Sık kullanılan ve elenecek kelimeler
        testStopwords = List.of("bir", "ve", "ile", "nedir", "icin", "olan");

        // 2. Suffixes: Kök bulma için kullanılacak ekler (Karışık sırayla veriyoruz, constructor sıralamalı)
        testSuffixes = List.of("lar", "den", "ler", "imiz", "iniz");

        // 3. Boosters: Niyete göre eklenecek kelimeler
        testBoosters = Map.of(
            Intent.STAFF_LOOKUP, List.of("staff", "contact", "email"),
            Intent.REGISTRATION, List.of("kayit", "dates")
        );

        // 4. Writer'ı Başlat
        writer = new HeuristicQueryWriter(testStopwords, testBoosters, testSuffixes, testMaxTerms);
    }

    @Test
    void testBasicProcessing_StopwordsAndLowercase() {
        // Senaryo: Stopword'ler silinmeli, noktalama kalkmalı, hepsi küçük harf olmalı.
        Context context = new Context("Mazeret sinavi ve basvuru icin surec nedir?");
        context.setCurrentIntent(Intent.UNKNOWN); // Niyet Boosting yok

        writer.execute(context);
        
        List<String> result = context.getQueryTerms();
        
        // Beklenen: "ve", "icin", "nedir" silinir.
        List<String> expected = List.of("mazeret", "sinavi", "basvuru", "surec");
        
        assertEquals(expected, result, "Stopword'ler silinmeli ve metin temizlenmeli.");
    }

    @Test
    void testIterativeStemming() {
        // Senaryo: "evlerimizden" -> (den) -> "evlerimiz" -> (imiz) -> "evler" -> (ler) -> "ev"
        // Constructor'ın ekleri uzunluklarına göre sıraladığını ve döngünün çalıştığını test eder.
        Context context = new Context("evlerimizden gelen haberler");
        context.setCurrentIntent(Intent.UNKNOWN);

        writer.execute(context);
        List<String> result = context.getQueryTerms();

        assertTrue(result.contains("ev"), "Kök 'ev' bulunmalı (ev-ler-imiz-den).");
        assertFalse(result.contains("evlerimizden"), "Orijinal kelime kalmamalı.");
        assertTrue(result.contains("haber"), "Kök 'haber' bulunmalı (haber-ler).");
    }

    @Test
    void testIntentBoostingPriority() {
        // Senaryo: Intent STAFF_LOOKUP. Booster'lar (staff, contact, email) başa gelmeli.
        // Soru içinde geçen "hocanin" kelimesi sonda kalmalı.
        Context context = new Context("Hocanin iletisim adresi");
        context.setCurrentIntent(Intent.STAFF_LOOKUP);

        writer.execute(context);
        List<String> result = context.getQueryTerms();

        // 1. Booster Kontrolü
        assertEquals("staff", result.get(0));
        assertEquals("contact", result.get(1));
        assertEquals("email", result.get(2));
        
        // 2. Orijinal Kelime Kontrolü
        assertTrue(result.contains("hocanin"));
        
        // 3. Toplam Boyut (3 booster + 3 kelime = 6)
        assertEquals(6, result.size());
    }

    @Test
    void testBoostingWithReplacement() {
        // Senaryo: Booster kelimesi ("staff") zaten soruda geçiyor.
        // Bu durumda "staff" kelimesi sorudan silinip, booster olarak BAŞA eklenmeli.
        Context context = new Context("staff odasi nerede");
        context.setCurrentIntent(Intent.STAFF_LOOKUP);

        writer.execute(context);
        List<String> result = context.getQueryTerms();

        // "staff" en başta olmalı (index 0)
        assertEquals("staff", result.get(0));
        
        // Listede sadece 1 tane "staff" olmalı (tekrarlamamalı)
        long staffCount = result.stream().filter(s -> s.equals("staff")).count();
        assertEquals(1, staffCount, "'staff' kelimesi listede sadece bir kez geçmeli.");
    }

    @Test
    void testMaxTermsLimit() {
        // Senaryo: 12 kelimelik bir soru. Max limit 10.
        Context context = new Context("bir iki uc dort bes alti yedi sekiz dokuz on onbir oniki");
        context.setCurrentIntent(Intent.UNKNOWN);

        writer.execute(context);
        List<String> result = context.getQueryTerms();

        assertEquals(10, result.size(), "Sonuç listesi maxTerms (10) ile sınırlanmalı.");
        assertTrue(result.contains("on"), "10. kelime dahil edilmeli.");
        assertFalse(result.contains("onbir"), "11. kelime atılmalı.");
    }

    @Test
    void testMaxTermsLimitWithBoosting() {
        // Senaryo: 3 Booster eklenecek. Soru 9 kelime. Toplam 12 potansiyel.
        // Sonuç 10 olmalı. Booster'lar kalmalı, sorunun sonundaki kelimeler atılmalı.
        Context context = new Context("a b c d e f g h i"); // 9 kelime
        context.setCurrentIntent(Intent.STAFF_LOOKUP); // +3 Booster (staff, contact, email)

        writer.execute(context);
        List<String> result = context.getQueryTerms();

        assertEquals(10, result.size());
        
        // Booster'lar başta mı?
        assertEquals("staff", result.get(0));
        
        // Sorunun başındaki kelimeler duruyor mu?
        assertTrue(result.contains("a"));
        
        // Sorunun sonundaki kelimeler atıldı mı? (Limit 10 olduğu için 'h' ve 'i' atılmalı)
        // [staff, contact, email, a, b, c, d, e, f, g] -> Toplam 10
        assertFalse(result.contains("h"));
        assertFalse(result.contains("i"));
    }
    
    @Test
    void testUniqueness() {
        // Senaryo: Aynı kelime birden fazla geçiyor.
        Context context = new Context("kayit ve kayit islemleri");
        context.setCurrentIntent(Intent.UNKNOWN);
        
        writer.execute(context);
        List<String> result = context.getQueryTerms();
        
        // 'kayit' sadece 1 kez olmalı
        assertEquals(1, result.stream().filter(s -> s.equals("kayit")).count());
        assertEquals(2, result.size()); // [kayit, islemleri]
    }
    
    @Test
    void testEmptyContextSafety() {
        Context context = new Context(""); // Boş soru
        writer.execute(context);
        
        assertNotNull(context.getQueryTerms());
        assertTrue(context.getQueryTerms().isEmpty());
    }
}