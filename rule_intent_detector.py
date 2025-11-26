from typing import List, Dict, Optional
from detector.intent import Intent
from detector.intent_detector import IntentDetector
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from orchestrator.context import Context

class RuleIntentDetector(IntentDetector):
    """
    Kural tabanlı (keyword matching) Intent tespiti yapan sınıf.
    """

    def __init__(self, intent_rules: Optional[Dict[Intent, List[str]]] = None, priority: Optional[List[int]] = None):
        # Eğer None gelirse boş dict veya boş list atıyoruz 
        self.intent_rules = intent_rules if intent_rules is not None else {}
        self.priority = priority if priority is not None else []

    def execute(self, context: 'Context') -> None:
        # Context'ten soruyu al 
        question = context.original_question

        # Boş soru kontrolü
        if not question or not question.strip():
            context.current_intent = Intent.UNKNOWN
            return

        normalized_question = question.lower()
        candidates: List[Intent] = []

        # Kuralları tara (Keyword Matching)
        for intent, keywords in self.intent_rules.items():
            for keyword in keywords:
                if keyword.lower() in normalized_question:
                    candidates.append(intent)
                    break # Bu intent için bir keyword bulmak yeterli, diğerlerine bakmaya gerek yok

        # Aday yoksa UNKNOWN
        if not candidates:
            context.current_intent = Intent.UNKNOWN
            return

        # Tek aday varsa direkt ata
        if len(candidates) == 1:
            context.current_intent = candidates[0]
            return

        # Öncelik Kontrolü (Priority Handling)
        if self.priority:
            # Python Enum'ları Java gibi ordinal ile çalışmaz, listeye çevirip index ile erişiyoruz
            all_intents = list(Intent)
            
            for intent_ordinal in self.priority:
                # Array indexi Enum sınırları içinde mi?
                if 0 <= intent_ordinal < len(all_intents):
                    priority_intent = all_intents[intent_ordinal]
                    
                    # Eğer öncelik listesindeki bu intent, adaylar arasındaysa kazanan odur.
                    if priority_intent in candidates:
                        context.current_intent = priority_intent
                        return

        # Fallback: Eğer öncelik listesi yoksa veya listedekiler adaylar arasında yoksa ilk adayı seç.
        context.current_intent = candidates[0]

    @property
    def name(self) -> str:
        return "intent_detector"
